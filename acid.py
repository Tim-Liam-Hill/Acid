import argparse
import re
import sys
import logging 
import json
from enum import Enum
import math

#Declaring as global since it is the definition of what symbols stand for
#Best keep it easily accessible and NOT duplicated 
#names are all lowercase since they correspond to terminals in the CFG in which are all
#lowercase to better distinguish from non-terminals
#convenient thing about this variable: if I decide to swap opcode meanings around, I don't need to change the interpreter
#since it deals with labels instead of opcodes 
CODON_OPCODES = {
    "AAA":  ["funcstart1", "funcname", "funcstart1"], 
    "TTT":  ["funcstart1", "funcname", "funcstart1"], 
    "CAA":  ["funcend1", "funcname", "funcend1"], 
    "GTT":  ["funcend1", "funcname", "funcend1"], 
    "AAC":  "printnum",
    "TTG":  "printnum",
    "CAC":  "printchar",
    "GTG":  "printchar",
    "AAG":  ["callfunc1", "funcname", "callfunc1"], 
    "TTC":  ["callfunc1", "funcname", "callfunc1"], 
    "CAG":  "return",
    "GTA":  "return",
    "AAT":  ["push", "num"],
    "TTA":  ["push", "num"],
    "CAT":  "pop",
    "GTA":  "pop",
    "ACA":  "moves1s2", 
    "TGT":  "moves1s2", 
    "CCA":  "moves2s1",
    "GGT":  "moves2s1",
    "ACC":  "add",
    "TGG":  "add",
    "CCC":  "sub",
    "GGG":  "sub",
    "ACG":  "mult",
    "TGC":  "mult",
    "CCG":  "div",
    "GGC":  "div",
    "ACT":  "root",
    "TGA":  "root",
    "CCT":  "pow",
    "GGA":  "pow",
    "AGA":  "ifstart",
    "TCT":  "ifstart",
    "CGA":  "ifend",
    "GCT":  "ifend",
    "AGC":  "elif",
    "TCG":  "elif",
    "CGC":  "els",  #is meant to be 'els' not 'else' since the former is the terminal version, the latter the non-terminal version
    "CGC":  "els",
    "AGG":  "equals",
    "TCC":  "equals",
    "CGG":  "isempty", 
    "CGG":  "isempty", 
    "AGT":  "lessthan",
    "TCA":  "lessthan",
    "CGT":  "greaterthan", 
    "GCA":  "greaterthan", 
    "ATA":  "and",
    "TAT":  "and",
    "CTA":  "or", 
    "GAT":  "or", 
    "ATC":  "not",
    "TAG":  "not",
    "CTC":  "userin",
    "GAG":  "userin",
    "ATG":  "loopstart",
    "TAC":  "loopstart",
    "CTG":  "loopend", 
    "GAC":  "loopend", 
    "ATT":  "swap",
    "TAA":  "swap",
    "CTT":  "copys1",
    "GAA":  "copys1",
}
#TODO: add a dict for valid Non-terminals for better checking?? where to incorporate, in the parser 
#or implementation of non-terminal states? 
#maybe we need a way to reference the CFG in this file. Will think about this. 

#Is this class really necessary? The values only get used in one place (the switch statement in the parser)
#going to implement the interpreter without a similar enum class and see how I feel afterwards. One or the other will change
#TODO: read and decide on the above
class SLR_ACTIONS(Enum):
    GO = "go"
    SHIFT = "shift"
    REDUCE = "reduce"
    ACCEPT = "accept"
    ERROR = ""


RECIPRICOLS = {"A":"T", "T":"A", "C":"G","G":"C"}

SLR_TABLE = json.load(open("SLR_TABLE.json"))
SLR_START_STATE = "0-100-102-104-106-108-11-110-112-13-15-17-19-2-21-23-41-5-59-6-7-71-79-82-84-86-88-9-90-92-94-96-98" #TODO: find a more elegant way to record this in the SLR_TABLE json file
SLR_END_SYMBOL = "$$$" #TODO: also encode this in the SLR_TABLE.json
CFG_RHS_SEPARATOR = " " #TODO: also encode this into SLR_TABLE.json
#basically just make SLR_TABLE.json contain itself inside another json object with values for the above. Will
#add this once I know everything I need to add

def invertCodon(codon):
    #maybe there is a fancy way of doing this with string.replace()
    #but given codon length will always be 3, that's overkill
    new_codon = ""
    for c in codon:
        new_codon += RECIPRICOLS[c] 

    return new_codon 

"""
For custom Error messages in exceptions. I thought about putting this in a separate file and having
a different class for each type of exception, but that seems overkill for this project. If I was
going to do intense testing then sure, but for my purposes this is enough. 
"""
class AcidException(Exception): 
    def __init__(self, message):
        super().__init__(message) 

#Making this a separate class in case I want to change the number system in future. Then I can use dependency
#Injection in the interpreter (I heard dependency injection is all the rage at the moment)
class AcidNumber:
    BIN_MAPPING = {"00":"A", "01":"C", "10":"G", "11":"T"}
    ACID_MAPPING = {"A":"00", "C":"01", "G":"10", "T":"11"}

    def __init__(self, numlength=15):
        self.ACID_NUM_LENGTH = numlength
        self.ACID_NUM_MAX = 4**(numlength-1) -1 #maximum value for any number if we allow for 15 codon long numbers (first codon is sign codon)
        self.ACID_NUM_MIN = -1 * (self.ACID_NUM_MAX)

    def intToAcid(self, i): #probably not needed, copied over from util fil
        ans = ""
        if(i<0):
            lead = "C" #TODO: maybe don't hardcode this
        else: lead = "A" #or this 

        temp = format(abs(i), 'b')
        temp = ("0" * (len(temp) % 2)) + temp #The fact that this is valid python code is wild to me
        
        for i in range(0,len(temp),2):  #is there a cool one-liner for this? 
            ans = ans + AcidNumber.BIN_MAPPING[temp[i:i+2]]
        
        return lead + ("A" * (14 - len(ans))) + ans

    def acidToInt(self, num): 
        if(len(num) != self.ACID_NUM_LENGTH): #this exception should never be thrown unless somehow an AST is provided to the interpreter that didn't come from the Parser
            raise AcidException("Acid number does not consist of the correct number of codons")

        #the method I am using here is just for convenience.
        #I am basically converting each symbol to it's binary equivalent and going to integer from there
        if(num[0] == "A" or num[0] == "C"):
            multiplier = -1 if num[0] == "C" else 1

            ans = ""
            for i in range(1,len(num)):
                ans = ans + AcidNumber.ACID_MAPPING[num[i]]
            return int(ans,2)*multiplier

        else: #handles 'reciprocol' numbers TODO: more testing 
            multiplier = -1 if num[0] == "G" else 1

            ans = ""
            for i in range(1,len(num)):
                ans = ans + AcidNumber.ACID_MAPPING[num[i]]
            return (self.ACID_NUM_MAX - int(ans,2))*multiplier

class Token: #Tokens that are stored by Nodes of the AST

    next_id = 1
    #Each Token needs to store:
    #-the command type
    #optionally, the value (for most it will be None)
    def __init__(self, label, value=None):
        self.id = Token.next_id
        Token.next_id += 1 

        self.label = label
        self.value = value

    def __str__(self):
        return "(ID: " + str(self.id) + ", Label: " + self.label + ", Value: " + str(self.value) +")"
    
    def __repr__(self):
        return "(ID: " + str(self.id) + ", Label: " + self.label + ", Value: " + str(self.value) +")"

class ASTNode: #node for the AST 

    next_id = 1

    def __init__(self, token):
        self.children = []
        self.token = token 
        self.id = ASTNode.next_id 
        ASTNode.next_id += 1 

    def __str__(self):
        val =""
        if(self.token.value != None):
            val = ", VALUE: " + self.token.value
        return "(ID: " + str(self.id) + " LABEL: " + str(self.token.label) +val+ ", CHILDREN: " + str(len(self.children)) + ")"
    
    def __repr__(self):
        val =""
        if(self.token.value != None):
            val = ", VALUE: " + self.token.value
        return "(ID: " + str(self.id) + " LABEL: " + str(self.token.label) +val+ ", CHILDREN: " + str(len(self.children)) + ")"    
    
    def print(self):
        self.printRecursive(1) 
    
    def printRecursive(self,level):
        print(" "*level + "|- " + str(self))
        for node in self.children:
            node.printRecursive(level +1)


#thought: gonna keep this simple but do we need to worry about reading in file line by line?
#I just want to read everything in all at once, and is it really likely that a single file is larger
#in size than the memory of the machine this program is running on? --maybe, but that will be considered
#and end user problem <o.o>
"""
Normally a DFA would be needed to handle the Lexical Analysis portion but since my language 
consists of 3 length char opcodes, it is easier to handle this with a while loop and dictionary.
TODO: decide what checking is done here?
""" 
class Scanner: #handles Lexical Analysis

    def __init__(self): 
        pass 

    def run(self, file_path, num_codons): #TODO: let this take in the mode so it can handle DNA mode
        return self.tokenize(file_path, num_codons)

    def tokenize(self, file_path, num_codons): 

        cleaned_code = ""
        try: 
            f = open(file_path)
            raw_code = f.read()
            cleaned_code = re.sub('[^ACGT]', '',raw_code)

        except IOError:
            logging.error("Could not open/read file: ", file_path)
            sys.exit()

        #I don't feel like putting everything inside the try-catch. Only want that portion to handle the 
        #reading section.

        if(len(cleaned_code) % 3 != 0):
            err = "Cleaned code length is not multiple of 3, that is NOT scientifically possible."
            raise AcidException(err)
            
        i = 0 
        tokens = []

        while(i!=len(cleaned_code)):
            next_codon = cleaned_code[i:i+3]
            logging.debug("Scanner.tokenize: codon: " + str(i//3) + " " + next_codon)

            #Need a special case for functions and numbers (push ops)
            FUNCS = ["AAA","TTT","CAA","GTT", "AAG", "TTC"]
            PUSH = ["AAT", "TTA"]
            if(next_codon in FUNCS):
                #Need to extract function name, neater to put that in a separate function  
                node_list, index = self.extractFunctionNodes(next_codon, cleaned_code, i)

                for node in node_list:
                    tokens.append(node)

                i = index #set i to the start of funcname_end codon so we don't iterate over function_name 

            elif(next_codon in PUSH):

                nodes = self.extractNumber(cleaned_code,next_codon,i,num_codons)
                for n in nodes:
                    tokens.append(n)
                i += num_codons*3
                
            else: 
                tokens.append(Token(CODON_OPCODES[next_codon]))

            i += 3 
        return tokens 

    def extractNumber(self, cleaned_code,next_codon,i,num_codons): 
        if(len(cleaned_code) < i+3+3*(num_codons)): #TODO: check this math 
            err = "Number " + cleaned_code[i+3:] + " is not of length " + str(num_codons) + " codons"
            raise AcidException(err)

        opcodes = CODON_OPCODES[next_codon]
        logging.debug("Extracted Number: " + cleaned_code[i+3:i+3+3*num_codons])
        return[Token(opcodes[0]),Token(opcodes[1], cleaned_code[i+3:i+3+3*num_codons])]
        
    
    #are we allowing empty function names? I guess so, since they are technically a palindrome. 
    def extractFunctionNodes(self, next_codon, cleaned_code, i): 
        logging.debug("Scanner.extractFunctionNodes: extracting function name")

        k = i + 3
        func_name = "" 
        recip = invertCodon(next_codon)
        while(k != len(cleaned_code) and cleaned_code[k:k+3] not in [next_codon, recip] ): 
            func_name += cleaned_code[k:k+3]
            k += 3

        if(k == len(cleaned_code)):
            #throw error, there is no closing tag for function name 
            err = "Function name does not have a closing tag, that is a bad thing in general"

            if(len(func_name) >=6):
                err = err + "\nCheck function with name: " + func_name[i+3:i+9] 
            else: err = err + "\nCheck function with name: " +  func_name
            raise AcidException(err)
        
        if(func_name != func_name[::-1]):
            err = "Function name '" + func_name +"' is not a palindrome. That isn't in the Spirit of Acid"
            err = err + "\nPlease ensure all function names are palindromes or alter the source code to remove this check"
            raise AcidException(err)

        not_allowed_codons = ["AAA", "TTT", "CAA", "GTT", "AAG", "TTC", "CAG", "GTA"]

        for codon in not_allowed_codons:
            for i in range(0, len(func_name), 3): #check only codons, not the entire string.
                if(codon in func_name[i:i+3]):
                    err = "Function name '" + func_name +"' contains codon '" + codon + "'"
                    err += "\nThis will lead to errors. Please adjust this function name to remove the offending codon"
                    raise AcidException(err) 
        
        terminals = CODON_OPCODES[next_codon]
        nodes = [Token(terminals[0]), Token(terminals[1], func_name), Token(terminals[2])]

        return nodes, k

#TODO: consider 'pruning the ast as we create it. It isn't strictly necessary but may make the resulting AST easier to read (and will reduce)
#its size somewhat). Doing this would require altering the parser (best to finish it first)
class Parser: #Handles Syntax analysis and builds an AST

    def __init__(self):
        self.Node = None
    
    def run(self, tokens):
        return self.buildAST(tokens)

    def buildAST(self, tokens):
        stack = [SLR_START_STATE]
        tokens.append(Token(SLR_END_SYMBOL))

        while(len(stack) != 0):
            logging.debug("Stack: " + str(stack))
            logging.debug("Tokens: " + str(tokens))
            
            state = stack[len(stack) -1]
            token = tokens[0]

            if(len(SLR_TABLE[state][token.label]) == 0 ): #TODO: change this once explicit error messages have been put into the SLR_TABLE json
                err = "No valid transition in SLR table for state " + str(state) + " and token " + str(token) + ", input is not a Acid program"
                err += "\nState: " + str(state) + " Token: " + str(token)
                raise AcidException(err) 
            
            match SLR_TABLE[state][token.label][0]:
                case SLR_ACTIONS.SHIFT.value: 
                    logging.debug("Shifting for state " + str(state) + " and token " + str(token))
                    stack.append(ASTNode(token))
                    stack.append(SLR_TABLE[state][token.label][1]) #pushing the next state to follow
                    tokens.pop(0)

                case SLR_ACTIONS.REDUCE.value: #TODO: clean up into a separate function, will make things look better
                    logging.debug("Reducing for state " + str(state) + " and token " + str(token) + " with production " + SLR_TABLE[state][token.label][1][0] + ":=" +SLR_TABLE[state][token.label][1][1] )
                    expected_elements = SLR_TABLE[state][token.label][1][1].split(CFG_RHS_SEPARATOR)
                    prod_length = len(expected_elements) if expected_elements[0] != '' else 0 #a check for empty productions (eg: R:=)
                    popped_elements = stack[len(stack) -2*prod_length:]
                    stack = stack[0:len(stack) -2*prod_length]
                    
                    node = ASTNode(Token(SLR_TABLE[state][token.label][1][0])) #creates a new token based on non-terminal on RHS of production
                    for i in range(prod_length):
                        if(popped_elements[2*i].token.label != expected_elements[i]):
                            err = "Error when reducing: stack tokens do not align with tokens production can produce"
                            raise AcidException(err)
                        node.children.append(popped_elements[2*i]) #append the popped elements since that is where the tokens are

                    go_state = SLR_TABLE[stack[len(stack)-1]][SLR_TABLE[state][token.label][1][0]]
                    logging.debug("Go state after reduction is: " + str(go_state))
                    
                    if(len(go_state) == 0 or go_state[0] != SLR_ACTIONS.GO.value):
                        err = "Error when reducing: invalid 'go' state to follow after reducing by production"
                        err += "\nThis is likely due to a malformed SLR table"
                        raise AcidException(err)

                    stack.append(node) 
                    stack.append(go_state[1])
                     
                case SLR_ACTIONS.ACCEPT.value:
                    return stack[1]

                case _:
                    err = "No matching action in SLR table with name " + str(SLR_TABLE[state][token.label][0])
                    err += "SLR table is malformed"
                    raise AcidException(err)

#Going to do this mostly by intuition: I have written an interpreter before in University and I don't
#believe the implementation of this language requires anything particularly                 
class Interpreter:


    FUNC_START_LABEL = "FUNCSTART"
    FUNC_END_LABEL = "FUNCEND"

    def __init__(self, acid_number):
        """
        An explanation is required for the below 2 variables.
        I considered creating a separate class for the symbol table but this seems like overkill. I only
        need to keep track of function names.
        The idea is to have a dictionary. The each time you define a function, you add that function name
        to the dictionary, map the name to the AST node where the function begins and enter its scope. 
        You remain in this scope until the function end is reached, after which you exit. If while inside a 
        function's scope another function is declare we do the same only this function name is defined inside 
        the previous function's entry in the map. So
        {
            func1: {
                node: ASTNode-reference,
                func2:{
                    node: ASTNode-reference
                }
            }
        }
        We then have a stack to hold the current scope we are in (ie: it holds the sub dict at name <funcname>).
        """
        self.func_mapping = {} 
        self.scope = [{}]
        self.acid_number = acid_number
        
        
    #It would be easiest to do this with recursion but I think it would be fun to try using a stack
    #there may be a more performant way of doing this (since right now I am storing references to dicts
    #on the stack) but I don't know if thats needed. We could store funcnames on the stack and use that
    #to build up but I don't think that's necessary here. In the interpreter itself it may be since
    #we will be handling function calls 
    #How to check that the end tag for an inner function does not fall outside an outer function:
    """
    Since the rule in the CFG is 
    FUNC:=FUNCSTART FUNCBODY FUNCEND
    we can just check that the next funcend has the same name as the function we are describing, if it doesn't
    then we don't have function name tags in the correct order 
    """
    #the last element left on the scope table becomes our mapping table for future use.
    def createFuncMapping(self, AST):
        logging.debug("Building the symbol table before running the program")
        stack = [AST] #the stack for symbols, not to be confused with the stacks the user code operates on

        while(len(stack) != 0):

            node = stack.pop()
 
            if(node.token.label == Interpreter.FUNC_START_LABEL):
                funcname = node.children[1].token.value 
                end_funcname = stack[len(stack)-2].children[1].token.value #the name for the ENDFUNC node
                logging.debug("Node " + str(node) + " defines start of a function with name " + funcname + ", adding to symbol table")
                
                if(end_funcname != funcname): #check that the FUNCNAME's second child value matches start tag funcname
                    err = "Function with name '" + funcname + "' has matching end tag with name '" +  end_funcname
                    err += "'\nThis implies that function '" + end_funcname + "' does not have its end tag defined within the function body of '"+funcname + "'"
                    raise AcidException(err)

                for s in self.scope[::-1]:
                    if(funcname in s):
                        err = "Redefinition of function " + funcname + " in the same/shared scope"
                        raise AcidException(err)
                
                
                new_scope = {"funcbody": stack[len(stack)-1]}
                self.scope[len(self.scope)-1][funcname] = new_scope
                self.scope.append(new_scope)

            elif(node.token.label == Interpreter.FUNC_END_LABEL):
                logging.debug("Node " + str(node) + " defines end of a function, exiting its scope")
                self.scope.pop()
            else:
                stack += node.children[::-1] #append in reverse order so they appear in order on the stack

        self.func_mapping = self.scope.pop() #empties the scope
        logging.debug("Function Symbol table complete: " + str(self.func_mapping))

    #TODO: introduce modes of running that control whether or not we print numbers as ACID base 4 numbers 
    #or regular numbers 
    def run(self, AST): 
        
        self.createFuncMapping(AST) #TODO: we will only be pushing references onto the stack each time we enter a scope, so that shouldn't be
                                    #too bad performance wise right?? May need to check this and reimplement if that isn't the case
        self.scope = [self.func_mapping] #reset the scope table tracker in case this function is called multiple times 
        stack = [ast]
        s1 = []
        s2 = []
        logging.debug("--- Interpreting input AST ---")

        while(len(stack) != 0):
            logging.info("s1: " + str(s1))
            logging.info("s2 reversed: " + str(s2[::-1]))
            logging.debug("stack: " + str(stack))
            node = stack.pop()

            """
            The only symbols we need to bother with implementing functions for are:
            IF (which can handle the sub elifs and such)
            LOOP
            STACK
            MATH
            IO
            CALLFUNC
            FUNC ->special case, we basically ignore these since they only get executed when called 
            """
            match node.token.label: 
                case "IF":
                    self.If(s1, s2, stack, node) #feels strange to pass in ASTNode stack into this function but it keeps the switch case cleaner
                                             #and the logic for if statements requires possible alteration of the stack
                case "LOOP":
                    #basically, check bool condition and if true push loop node back onto stack, followed by pushing loopbody
                    self.loop(s1, s2, stack, node)
                case "STACK":
                    self.stack(s1,s2,node)
                case "MATH":
                    self.math(s1,s2,node)
                case "IO":
                    self.io(s1,node)
                case "CALLFUNC":
                    self.callFunc(stack, node)
                case "FUNCBODY":
                    self.funcBody(stack,node)
                case "FUNC":
                    pass #ignore FUNC nodes
                case _: #just add the children of the current node onto the stack 
                    logging.debug("Default case for node " + node.token.label +", adding its children to the stack")
                    stack += node.children[::-1]
                    
    #any number that is on the stack will be not in Acid base 4 form, but will be normal integers
    #any handling of numbers 
    def math(self, s1, s2, node):

        logging.debug("Performing math operation: " + node.children[0].token.label)
        #all of the below operations require 2<= elements on s1, so we can do the 
        #error check once before the switch case
        if(len(s1) < 2):
            err = "Attempting to perform action '" + node.children[0].token.label + "' on s1 which "
            err += "only has length " + str(len(s1))
            raise AcidException(err)
        
        num1 = s1.pop()
        match node.children[0].token.label:
            case "add":  
                s1.append(num1 + s1.pop())
            case "sub":
                s1.append(num1 - s1.pop())
            case "mult":
                s1.append(num1 * s1.pop())
            case "div":
                num2 = s1.pop()
                if(num2 == 0): #Python would throw an exception but its better for my own language to throw this error 
                    raise AcidException("Attempting to divide by zero")
                s1.append(num1 // num2)
                s2.append(num1 % num2)
            case "root":
                #TODO: what extra checks do we want to put here?
                num2 = s1.pop()
                if(num1 < 0): 
                    if(num2 % 2 == 0):
                        raise AcidException("Cannot find nth power of a negative number when n is even")
                    root = math.floor((-1*num1)**(1/num2))
                    rem = num1 + root**(num2)
                    s1.append(root)
                    s2.append(rem)
                else: 
                    root = math.floor(num1**(1/num2))
                    rem = num1 - root**(num2)
                    s1.append(root)
                    s2.append(rem)

            case "pow":
                s1.append(num1**(s1.pop))
            case default: 
                err = "Found symbol '" + node.children[0].token.label + "' which is not a valid symbol for mathematical operations"
                raise AcidException(err) 

    #TODO: check if there are more efficient operations to use when manipulating stack (eg: pop vs some other)
    #method. Granted, performance isn't really the goal but it could still be interesting to look into
    def stack(self, s1, s2, node):
        logging.debug("Performing stack operation: " + node.children[0].token.label)
        
        match node.children[0].token.label:
            
            case "push":
                s1.append(self.acid_number.acidToInt(node.children[1].token.value))
            case "pop":
                if(len(s1) <= 0):
                    raise AcidException("Cannot pop element from empty stack")
                s1.pop()
            case "moves1s2":
                 if(len(s1) <= 0):
                    raise AcidException("Cannot move element from s1 to s2: s1 is empty")
                 s2.append(s1.pop())
            case "moves2s1":
                if(len(s2) <= 0):
                    raise AcidException("Cannot pop element from empty stack")
                s1.append(s2.pop())
            case "copys1":
                if(len(s1) <= 0):
                    raise AcidException("Cannot copy element from s1: stack is empty")
                s2.append(s1[len(s1)-1])
            case "swaps1s2":
                if(len(s1) <= 0 or len(s2) <=0):
                    raise AcidException("Cannot swap elements of stacks when one stack is empty")
                temp = s1.pop()
                s1.append(s2.pop())
                s2.append(temp)
            case "swapfirstlasts1":
                if(len(s1) < 1):
                    raise AcidException("Cannot swap first and last element of s1 when s1 is empty")
                if(len(s1) != 1): #only swap if it would change the stack
                    temp = s1[len(s1)-1]
                    s1[len(s1)-1] = s1[0]
                    s1[0] = temp
            case _:
                err = "Found symbol '" + node.children[0].token.label + "' which is not a valid symbol for stack operations"
                raise AcidException(err) 

    #TODO: allow for output to be sent somewhere besides console? would help for testing
    #maybe allow for overriding sys.stdout
    def io(self, s1, node):
        logging.debug("Performing IO operation: " + node.children[0].token.label)
        match node.children[0].token.label:
            case "userin":
                i = input("")
                try:
                    num = int(i)
                    if(num > self.acid_number.ACID_NUM_MAX or num < self.acid_number.ACID_NUM_MIN):
                        raise ValueError("")

                    logging.debug("Userinput interpreted as integer with value " + str(num))
                    s1.append(num)
                except ValueError: 
                    logging.debug("Userinput interpreted as string, each char will have ascii value pushed on stack")
                    for char in i:
                        s1.append(ord(char))
            case "printnum":
                print(s1[len(s1)-1], end="")
                
            case "printchar":
                print(chr(s1[len(s1)-1]), end="") #TODO: do we need error checking for the chr function?
            case _:
                err = "Found symbol '" + node.children[0].token.label + "' which is not a valid symbol for sIO operations"
                raise AcidException(err) 

    def If(self, s1, s2, stack, node):
        logging.debug("Evaluating If statement")
        ifbody = node.children[2]
        if(self.boolean(s1,s2,node.children[1])):
            stack.append(ifbody.children[0]) #push the code to be executed onto stack in event of true evaluation
            return #in my opinion, preventing indenting the rest of the below code with an 'else' statement leads to code
                   #that is easier to read visually
        
        match len(ifbody.children): #if bool is false, action we take is determined by structure of trailing 'else-if's and 'else' 
            case 2: #check if the else is 'empty' (ie: no else) 
                if(len(ifbody.children[1].children) != 0):
                    stack.append(ifbody.children[1].children[1])
            case 4: 
                self.elseIf(s1,s2,stack,ifbody) #easier to handle this case with a recursive function
            case _:
                raise AcidException("Malformed Boolean expresssion: body of if-statement must have 2 or 4 child nodes. Likely not an issue with input program")

    def elseIf(self, s1, s2, stack, node):
        logging.debug("Evaluating else-if statement")
        ifbody = node.children[3]
        if(self.boolean(s1,s2,stack, node.children[2])):
            stack.push(ifbody.children[3]) 
            return 
        
        match len(ifbody.children): 
            case 2: 
                if(len(ifbody.children[1].children) != 0):
                    stack.push(ifbody.children[1].children[1])
            case 4: 
                self.elseIf(s1,s2,stack,ifbody) #easier to handle this case with a recursive function
            case _:
                raise AcidException("Malformed Boolean expresssion: body of if-statement must have 2 or 4 child nodes. Likely not an issue with input program")

    def loop(self,s1,s2,stack, node):
        logging.debug("Evaluating while loop")
        if(self.boolean(s1,s2,node.children[1])):
            stack.append(node) 
            stack.append(node.children[2])

    #evaluates a boolean expression to return true or false 
    def boolean(self, s1, s2, node):
        #Case for what boolean expression we are dealing with is determined by num children of the boolean node
        logging.debug("Evaluating Boolean expression")

        match node.children[0].token.label: 
            case "equals":
                if(len(s1) <2):
                    raise AcidException("Cannot compare top 2 elements of s1 when s1 has less than 2 elements")
                return s1[len(s1)-1] == s1[len(s1)-2]
            case "lessthan":
                if(len(s1) <2):
                    raise AcidException("Cannot compare top 2 elements of s1 when s1 has less than 2 elements")
                return s1[len(s1)-2] < s1[len(s1)-1]
            case "greaterthan":
                if(len(s1) <2):
                    raise AcidException("Cannot compare top 2 elements of s1 when s1 has less than 2 elements")
                return s1[len(s1)-2] > s1[len(s1)-1]
            case "isemptys1":
                return len(s1) == 0
            case "isemptys2":
                return len(s2) == 0
            case "not":
                return not self.boolean(s1,s2,node.children[1])
            case _: 
                err = "Boolean expression has invalid keyword: " + node.children[0].token.label
                err += "\nThis is likely an issue with the created AST and not with the Acid code"
                raise AcidException(err)

    def callFunc(self, stack, node):
        funcname = node.children[1].token.value
        logging.debug("Calling function with name '" + funcname + "'")
        #first, check if the funcname is in one of the scopes we have entered 
        
        for scope in self.scope[::-1]:
            if(funcname in scope):
                stack.append(scope[funcname]["funcbody"])
                self.scope.append(scope[funcname])
                return 
        err = "Cannot call function with name'" + funcname + "', this name is not defined in any current scope"
        raise AcidException(err)

    def funcBody(self, stack, node):
        logging.debug("Evaluating code inside of a function's body")
        match len(node.children):
            case 0: #implicit return statement
                self.scope.pop()
            case 2:
                if(node.children[0].token.label == "return"):
                    self.scope.pop()
                    return 
                stack += node.children[::-1]
            case _:
                raise AcidException("Invalid function body")

class Acid: 

    def __init__(self): #IDEA: use dependency injection to make this more extensible in future
        pass 


if __name__=="__main__": 
    
    parser = argparse.ArgumentParser(description="Acid programming language interpreter")
    parser.add_argument("--input", dest='in_file', help="The location of the input file containing acid code.", required=True)
    parser.add_argument("--num_codons",dest='num_codons', help="The number of codons used for numbers (determines range of numerical values). Default = 5", default=5)
    parser.add_argument("--log",dest='log_level', help="The level for logging statements", default="ERROR")
    
    args = parser.parse_args()
    
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log_level)

    logging.basicConfig(level=numeric_level)
    scan = Scanner()
    tokens = scan.run(args.in_file, args.num_codons)
    #for n in tokens:
    #    print(n)
    
    parser = Parser()
    ast = parser.run(tokens)
    #ast.print()
    #print("-"*20)
    interpreter = Interpreter(AcidNumber(15))
    interpreter.run(ast)
    

    



