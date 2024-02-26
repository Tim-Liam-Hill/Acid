import argparse

import sys
import logging 
from acid import Acid

def main():
    parser = argparse.ArgumentParser(description="Acid programming language interpreter")
    parser.add_argument("--input", dest='in_file', help="The location of the input file containing acid code.", required=True)
    parser.add_argument("--num_codons",dest='num_codons', help="The number of codons used for numbers (determines range of numerical values). Default = 5", default=5)
    parser.add_argument("--log",dest='log_level', help="The level for logging statements", default="ERROR")
    
    args = parser.parse_args()
    
    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log_level)

    logging.basicConfig(level=numeric_level)
    acid = Acid(args)
    acid.run(args)

if __name__=="__main__": 
    main()

    