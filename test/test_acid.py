from src.acid.acid import *  
import pytest 


#TODO: test that all codons are defined at top of acid.py 

"""
Cases:
- empty input
- wrong number of nucleotides/not divisible by 3
- invalid function names (contains illegal sequences, missing end tags etc)
- number too short (not of correct length codons)
"""
class TestScanner:
    num_codons = 5
    scanner = Scanner() #Scanner doesn't hold any data, so we can just use one static scanner to ensure behaviour is the same
                        #faster than recreating a new scanner for each test
    
    def test_empty(self):
        input = ""
        
        tokens = TestScanner.scanner.run(input, TestScanner.num_codons)
        assert tokens == []
    
    def test_ensureNonNucleotidesAreDropped(self):
        input = "CGG@#$%^&*())alstcioonc189723vblkc,bd';}[.mvb'a?.<>]_-=+,"
        
        tokens = TestScanner.scanner.run(input, TestScanner.num_codons)
        assert tokens == [Token("isemptys1")]

    def test_notDivisibleBy3(self):
        input = "ACG GTC C" #spaces are for readibility only
        
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Cleaned code length is not multiple of 3, at least one codon is malformed."
    
    def test_notPalindrome(self): #possibly the most important test of all, checks that function names must be palindromes
        input = "AAA CAT AAA" 
        
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input, TestScanner.num_codons)
        assert exc_info.value.args[0] =="Function name 'CAT' is not a palindrome. That isn't in the Spirit of Acid\nPlease ensure all function names are palindromes or alter the source code of Acid to remove this check"

    def test_emptyFunctionName(self):
        input = "AAA AAA CAA CAA"
        
        tokens = TestScanner.scanner.run(input, TestScanner.num_codons)
        assert tokens == [Token("funcstart1"), Token("funcname", ""), Token("funcstart1"), Token("funcend1"), Token("funcname",""),Token("funcend1")]

    def test_invalidCodonInFuncName(self): #testing all 8 cases of which codons cannot be in a function name
        #the error for invalid codons present comes after the check for palindrome so these names must
        #be palindromes to avoid triggering that error
        input1 = "AAA GTT TTG AAA"
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input1, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name 'GTTTTG' contains codon 'GTT'\nThis will lead to errors. Please adjust this function name to remove the offending codon"
    
        input2 = "TTT AAG GAA TTT"
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input2, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name 'AAGGAA' contains codon 'AAG'\nThis will lead to errors. Please adjust this function name to remove the offending codon"
    
        input3 = "CAA CAG GAC CAA"
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input3, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name 'CAGGAC' contains codon 'CAG'\nThis will lead to errors. Please adjust this function name to remove the offending codon"
    
        input4 = "GTT GTA ATG GTT"
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input4, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name 'GTAATG' contains codon 'GTA'\nThis will lead to errors. Please adjust this function name to remove the offending codon"
    
        input5 = "AAG AAA AAA AAG"
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input5, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name 'AAAAAA' contains codon 'AAA'\nThis will lead to errors. Please adjust this function name to remove the offending codon"
    
        input6 = "TTC TTT TTT TTC"
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input6, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name 'TTTTTT' contains codon 'TTT'\nThis will lead to errors. Please adjust this function name to remove the offending codon"
    
        input7 = "AAA CAA AAC AAA"
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input7, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name 'CAAAAC' contains codon 'CAA'\nThis will lead to errors. Please adjust this function name to remove the offending codon"
    
        input8 = "AAA TTC CTT AAA"
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input8, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name 'TTCCTT' contains codon 'TTC'\nThis will lead to errors. Please adjust this function name to remove the offending codon"
    
    def test_numTooShort(self):
        input1 = "AAT AAA AAA AAA AAA" #this exception only occurs if the last operation involves a number. Normally it would result in incorrect app behaviour instead
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input1, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Number AAAAAAAAAAAA is not of length 5 codons"
    
    #below ensures that errors are thrown if there is no matching end tag func related opcodes
    def test_missingMatchingEndTag(self):
        input1 = "AAA CAT TAC" #this exception only occurs if the last operation involves a number. Normally it would result in incorrect app behaviour instead
        with pytest.raises(AcidException) as exc_info:
            tokens = TestScanner.scanner.run(input1, TestScanner.num_codons)
        assert exc_info.value.args[0] == "Function name does not have a closing tag\nCheck function with name: CATTAC"

"""
Test Cases (not exhaustive):
- Missing end tags (functions, loops, if)
- else without if
- Functions declared incorrectly (end tag not in correct scope)
- Boolean 'not' not followed by another boolean
- missing boolean statements for if and while loops 
"""
class TestParser:

    def test2(self):
        pass

    def test_missingFunctionTags(self):
        pass 

    def test_missingIfTag(self):
        pass

    def test_ifWithoutElse(self):
        pass 

class TestInterpreter:

    pass
