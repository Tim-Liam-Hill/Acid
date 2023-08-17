import sys
import math

ALPHABET = {"A":0, "C":1, "G":2, "T":3}
TEBAHPLA = {0:"A", 1:"C", 2:"G", 3:"T"} # its for reverse conversion, so its backwards, geddit? 
num_bits = 15

# I started writing this code before I actually thought really hard about what I wanted. As a result, 
# I probably won't need any of this. 

def toSignedBase4(num): #basically: get magnitude of number. If negative, add 1 to magnitude and make sure leading is C 
    
    isnegative = False 
    if(num<1):
        isnegative = True 
        num *= -1 

    s = ""
    while(num > 4):
        
        s = str(num%4) + s
        num = int(num/4)
        print(num)
        print(s)
    s = str(num) + s 
    ans = ""
    
    print(s)

    if(isnegative):
        s = addOne(s)
        print(s)
        for i in s:
            ans += TEBAHPLA[int(i)]
        ans = "C" + ans
    else:
        for i in s:
            ans += TEBAHPLA[int(i)]
        ans = "A" + ans 
    return(ans)


def fromSignedBase4(s): 

    isnegative = False 

    if(s[0] != 'A'):
        isnegative =  True 

    s = s[1::] #get rid of sign 'bit'. If it is non 'A' it will be treated as 'C' regardless of what it actually was.

    #from letters to numbers
    new_s = ""
    for i in s:
        if(i not in ALPHABET):
            raise ValueError(i + " Not a valid letter")
        new_s = new_s + str(ALPHABET[i])
    

    if(isnegative):
        comp = complement(new_s) 
        subbed = subOne(comp) 
        new_s = subbed

    new_s = new_s[::-1] #reverse the string 

    total = 0    
    for i in range(len(new_s)):
        total += math.pow(4,i) * int(new_s[i])

    if(isnegative):
        total *= -1
    return total

def complement(s):

    ans = "" 

    for i in s: # the most hardcore coding you have ever seen in your life booooooiiiiiiiii 
        ans = ans + str(3-int(i))

    return ans 

def subOne(s): #who needs comments???
    #but seriously, takes a base 4 number in number form (no letters, just numbers)
    #Then subs 1 
    #If overflow then RIP I guess. 

    r = 1 
    ans = ""
    s = s[::-1]
    for i in s: 
        if(r != 1):
            ans = i + ans
        else: 
            if(i == "0"):
                ans = "3" + ans 
            else: 
                r = 0     
                ans = str(int(i) - 1) + ans  

    return ans  

def addOne(s): 
    
    ans = ""
    carry = 1 
    for i in s[::-1]:
        if(carry == 0):
            ans = ans + i
        else: 
            if(i == "3"):
                ans = ans + "0" 
            else:
                carry = 0
                ans = ans + str(int(i) + 1)

    return ans 

if __name__=='__main__':
    
    if(len(sys.argv) !=2):
        print("Usage: Base4Convert.py <num>")
        exit()

    s = sys.argv[1]
    if(s[0] in ALPHABET):
        print(fromSignedBase4(s))
    else: 
        print(toSignedBase4(int(s)))

    
            

