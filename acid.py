import argparse
import re
import sys
import logging 

#Declaring as global since it is the definition of what symbols stand for
#Best keep it easily accessible and NOT duplicated 
CODON_OPCODES = {
    "AAA":  "FUNCSTART", 
    "TTT":  "FUNCSTART", 
    "CAA":  "FUNCEND", 
    "GTT":  "FUNCEND", 
    "AAC":  "PRINTNUM",
    "TTG":  "PRINTNUM",
    "CAC":  "PRINTCHAR",
    "GTG":  "PRINTCHAR",
    "AAG":  "CALLFUNC", 
    "TTC":  "CALLFUNC", 
    "CAG":  "RETURN",
    "GTA":  "RETURN",
    "AAT":  "PUSH",
    "TTA":  "PUSH",
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


class Node: # node for the AST

    #Each node needs to store:
    #-the command type
    #
    def __init__(self):
        pass 


#thought: gonna keep this simple but do we need to worry about reading in file line by line?
#I just want to read everything in all at once.
"""
Normally a DFA would be needed to handle the Lexical Analysis portion but since my language 
consists of 3 length char opcodes, it is easier to handle this with a while loop and dictionary.
TODO: decide what checking is done here? Let's not check for matching function name declarators and other 
here. Let's do that in the Syntax phase.
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
            logging.error("Cleaned code length is not multiple of 3, that is NOT scientifically possible.")
            sys.exit()

        i = 0 
        while(i!=len(cleaned_code)):
            next_codon = cleaned_code[i:i+3]
            logging.debug("Scanner.tokenize: codon: " + str(i) + " " + next_codon)


            i += 3 


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
    scan.run(args.in_file, args.num_codons)

    



