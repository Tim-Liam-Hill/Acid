import argparse
import re
import sys
import logging 

#Declaring as global since it is the definition of what symbols stand for
#Best keep it easily accessible and NOT duplicated 
CODON_OPCODES = {
    "AAA":  ["FUNCSTART1", "FUNCNAME", "FUNCSTART1"], 
    "TTT":  ["FUNCSTART1", "FUNCNAME", "FUNCSTART1"], 
    "CAA":  ["FUNCEND1", "FUNCNAME", "FUNCEND1"], 
    "GTT":  ["FUNCEND1", "FUNCNAME", "FUNCEND1"], 
    "AAC":  "PRINTNUM",
    "TTG":  "PRINTNUM",
    "CAC":  "PRINTCHAR",
    "GTG":  "PRINTCHAR",
    "AAG":  ["CALLFUNC1", "FUNCNAME", "CALLFUNC1"], 
    "TTC":  ["CALLFUNC1", "FUNCNAME", "CALLFUNC1"], 
    "CAG":  "RETURN",
    "GTA":  "RETURN",
    "AAT":  ["PUSH", "NUMBER"],
    "TTA":  ["PUSH", "NUMBER"],
    "CAT":  "POP",
    "GTA":  "POP",
    "ACA":  "MOVES1S2", 
    "TGT":  "MOVES1S2", 
    "CCA":  "MOVES2S1",
    "GGT":  "MOVES2S1",
    "ACC":  "ADD",
    "TGG":  "ADD",
    "CCC":  "SUB",
    "GGG":  "SUB",
    "ACG":  "MULT",
    "TGC":  "MULT",
    "CCG":  "DIV",
    "GGC":  "DIV",
    "ACT":  "ROOT",
    "TGA":  "ROOT",
    "CCT":  "POW",
    "GGA":  "POW",
    "AGA":  "IFSTART",
    "TCT":  "IFSTART",
    "CGA":  "IFEND",
    "GCT":  "IFEND",
    "AGC":  "ELIF",
    "TCG":  "ELIF",
    "CGC":  "ELSE",
    "CGC":  "ELSE",
    "AGG":  "EQUALS",
    "TCC":  "EQUALS",
    "CGG":  "ISEMPTY", 
    "CGG":  "ISEMPTY", 
    "AGT":  "LESSTHAN",
    "TCA":  "LESSTHAN",
    "CGT":  "GREATERTHAN", 
    "GCA":  "GREATERTHAN", 
    "ATA":  "AND",
    "TAT":  "AND",
    "CTA":  "OR", 
    "GAT":  "OR", 
    "ATC":  "NOT",
    "TAG":  "NOT",
    "CTC":  "USERIN",
    "GAG":  "USERIN",
    "ATG":  "LOOPSTART",
    "TAC":  "LOOPSTART",
    "CTG":  "LOOPEND", 
    "GAC":  "LOOPEND", 
    "ATT":  "SWAP",
    "TAA":  "SWAP",
    "CTT":  "COPYS1",
    "GAA":  "COPYS1",
}

RECIPRICOLS = {"A":"T", "T":"A", "C":"G","G":"C"}

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

class Node: # node for the AST

    next_id = 1
    #Each node needs to store:
    #-the command type
    #optionally, the value (for most it will be None)
    def __init__(self, label, value=None):
        self.id = Node.next_id
        Node.next_id += 1 

        self.label = label
        self.value = value

    def print(self):
        print("Node: " + str(self.id) + ", Label: ", self.label + ", Value: " + str(self.value))



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

    def run(self, file_path, num_codons): #todo: let this take in the mode so it can handle DNA mode
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
                tokens.append(Node(CODON_OPCODES[next_codon]))

            i += 3 
        return tokens 

    def extractNumber(self, cleaned_code,next_codon,i,num_codons): 
        if(len(cleaned_code) < i+3+3*(num_codons)): #TODO: check this math 
            err = "Number " + cleaned_code[i+3:] + " is not of length " + str(num_codons) + " codons"
            raise AcidException(err)

        opcodes = CODON_OPCODES[next_codon]
        logging.debug("Extracted Number: " + cleaned_code[i+3:i+3+3*num_codons])
        return[Node(opcodes[0]),Node(opcodes[1], cleaned_code[i+3:i+3+3*num_codons])]
        
    
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
        nodes = [Node(terminals[0]), Node(terminals[1], func_name), Node(terminals[2])]

        return nodes, k


class Parser: #Handles Syntax analysis and builds an AST

    def __init__(self):
        pass 

    def buildAST(self, cleaned_code):
        pass 
        #basically: have a map for each token to what that function actually does. 

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
    
    """
    parser.add_argument("--output",dest='out_path', help="The location in s3 or hdfs where the output should be stored", required=True)
    parser.add_argument("--country-code", dest='country_code_path', help="The location of the file used to map ActionGeo_FeatureID to country codes", required=True)
    """
    args = parser.parse_args()
    
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log_level)

    logging.basicConfig(level=numeric_level)
    scan = Scanner()
    nodes = scan.run(args.in_file, args.num_codons)
    for n in nodes:
        n.print()

    



