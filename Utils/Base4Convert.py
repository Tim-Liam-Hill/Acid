import sys

BIN_MAPPING = {"00":"A", "01":"C", "10":"G", "11":"T"}
ACID_MAPPING = {"A":"00", "C":"01", "G":"10", "T":"11"}
ACID_NUM_LENGTH = 15
ACID_NUM_MAX = 268435455 # double check this. 

def intToAcid(i): #takes into account sign
    ans = ""
    if(i<0):
        lead = "C" #TODO: maybe don't hardcode this
    else: lead = "A" #or this 

    temp = format(abs(i), 'b')
    temp = ("0" * (len(temp) % 2)) + temp #The fact that this is valid python code is wild to me
    
    for i in range(0,len(temp),2):  #is there a cool one-liner for this? 
        ans = ans + BIN_MAPPING[temp[i:i+2]]
    
    return lead + ("A" * (14 - len(ans))) + ans

def acidToInt(num): 
    if(len(num) != ACID_NUM_LENGTH):
        raise "Incorrect length Acid number"

    #the method I am using here is just for convenience.
    #I am basically converting each symbol to it's binary equivalent and 
    if(num[0] == "A" or num[0] == "C"):
        multiplier = -1 if num[0] == "C" else 1

        ans = ""
        for i in range(1,len(num)):
            ans = ans + ACID_MAPPING[num[i]]
        return int(ans,2)*multiplier

    else: 
        multiplier = -1 if num[0] == "G" else 1

        ans = ""
        for i in range(1,len(num)):
            ans = ans + ACID_MAPPING[num[i]]
        return (ACID_NUM_MAX - int(ans,2))*multiplier

if __name__=="__main__" :
    if(len(sys.argv) != 2):
        print("Usage: Base4Convert.py <val>")
    
    try:
        print(intToAcid(int(sys.argv[1]))) 
    except ValueError: #I don't like the fact this is how we are doing this, but Python. 
        print(acidToInt(sys.argv[1]))

