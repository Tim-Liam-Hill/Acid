"""
A helper script I wrote so I didn't need to manually type out all combinations of Bases for opcodes
"""


LETTERS = ["A","C","G","T"]
AMINO_LENGTH = 3
OUT_FILE = "opcodes.txt"

def genAminoAcids(s, stack):
    if(len(s) == AMINO_LENGTH):
        stack.append(s)
        return 
    
    for i in LETTERS:
        genAminoAcids(s+i, stack)
    
if __name__=="__main__": 

    s = []
    genAminoAcids("",s) 
    print(s)
    f = open(OUT_FILE,"w")
    for i in s:
        f.write(i + "\n")

    f.close() 





