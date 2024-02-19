import argparse
import re
import sys
import logging 
import json
from enum import Enum

#Declaring as global since it is the definition of what symbols stand for
#Best keep it easily accessible and NOT duplicated 
#names are all lowercase since they correspond to terminals in the CFG which I made all 
#lowercase to better distinguish from non-terminals
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

class SLR_ACTIONS(Enum):
    GO = "go"
    SHIFT = "shift"
    REDUCE = "reduce"
    ACCEPT = "accept"
    ERROR = ""


RECIPRICOLS = {"A":"T", "T":"A", "C":"G","G":"C"}

SLR_TABLE = json.load(open("SLR_TABLE.json"))
SLR_START_STATE = "0-100-102-104-106-108-11-110-112-114-116-118-13-15-17-19-2-21-23-41-5-6-65-7-77-85-88-9-90-92-94-96-98" #TODO: find a more elegant way to record this in the SLR_TABLE json file
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

    def print(self):
        print("Token: " + str(self.id) + ", Label: ", self.label + ", Value: " + str(self.value))
    
    def __str__(self):
        return "(Token: " + str(self.id) + ", Label: " + self.label + ", Value: " + str(self.value) +")"
    
    def __repr__(self):
        return "(Token: " + str(self.id) + ", Label: " + self.label + ", Value: " + str(self.value) +")"

      

class ASTNode: #node for the AST 

    next_id = 1

    def __init__(self, token):
        self.children = []
        self.token = token 
        self.id = ASTNode.next_id 
        ASTNode.next_id += 1 

    def __str__(self):
        return "(ID: " + str(self.id) + " TOKEN: " + str(self.token) + " CHILDREN: " + str(self.children) + ")"
    
    def __repr__(self):
        return "(ID: " + str(self.id) + " TOKEN: " + str(self.token) + " CHILDREN: " + str(self.children) + ")"
    
    def printSimple(self):
        self.printSimpleRecursive(1)
    
    def printSimpleRecursive(self, level):
        print(" "*level + "|- " + str(self.token.label))
        for node in self.children:
            node.printSimpleRecursive(level +1)
        
    def print(self):
        self.printRecursive(1) 
    
    def printRecursive(self,level):
        print(" "*level + "|- " + str(self))
        for node in self.children:
            node.printRecursive(level +1)


#thought: gonna keep this simple but do we need to worry about reading in file line by line?
#I just want to read everything in all at once.
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

                    continue
                case SLR_ACTIONS.REDUCE.value: 
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

                    node.printSimple()
                    go_state = SLR_TABLE[stack[len(stack)-1]][SLR_TABLE[state][token.label][1][0]]
                    logging.debug("Go state after reduction is: " + str(go_state))
                    
                    if(len(go_state) == 0 or go_state[0] != SLR_ACTIONS.GO.value):
                        err = "Error when reducing: invalid 'go' state to follow after reducing by production"
                        err += "\nThis is likely due to a malformed SLR table"
                        raise AcidException(err)

                    stack.append(node) 
                    stack.append(go_state[1])
                    continue 
                case SLR_ACTIONS.ACCEPT.value:
                    return stack[1]

                case default:
                    err = "No matching action in SLR table with name " + str(SLR_TABLE[state][token.label][0])
                    err += "SLR table is malformed"
                    raise AcidException(err)
                    
class Interpreter:

    def __init__(self): 
        pass 

class Acid: 

    def __init__(self): #IDEA: use dependency injection to make this more extensible in future
        pass 


if __name__=="__main__": 
    
    parser = argparse.ArgumentParser(description="Acid programming language interpreter")
    parser.add_argument("--input", dest='in_file', help="The location of the input file containing acid code.", required=True)
    parser.add_argument("--num_codons",dest='num_codons', help="The number of codons used for numbers (determines range of numerical values). Default = 5", default=5)
    parser.add_argument("--log",dest='log_level', help="The level for logging statements", default="INFO")
    
    args = parser.parse_args()
    
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log_level)

    logging.basicConfig(level=numeric_level)
    scan = Scanner()
    tokens = scan.run(args.in_file, args.num_codons)
    for n in tokens:
        n.print()
    
    parser = Parser()
    ast = parser.run(tokens)
    ast.printSimple()
    

    



