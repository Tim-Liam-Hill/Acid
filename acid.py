import argparse
import re
import sys

#thought: gonna keep this simple but do we need to worry about reading in file line by line?
#I just want to read everything in all at once. 
class Scanner: #handles Lexical Analysis

    def __init__(self): 
        pass 

    def run(self, input): #todo: let this take in the mode so it can handle DNA mode
        return self.tokenize(input)

    def tokenize(self, file_path): 

        try: 
            f = open(file_path)
            raw_code = f.read()
            return re.sub('[^ACGT]', '',raw_code)
        except IOError:
            print("Could not open/read file: ", file_path)
            sys.exit()

class Node: # node for the AST

    def __init__(self):
        pass 

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
    """
    parser.add_argument("--output",dest='out_path', help="The location in s3 or hdfs where the output should be stored", required=True)
    parser.add_argument("--country-code", dest='country_code_path', help="The location of the file used to map ActionGeo_FeatureID to country codes", required=True)
    """
    args = parser.parse_args()
    
    scan = RegularScanner()
    print(scan.run(args.in_file))

    



