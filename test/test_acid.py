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

class TestParser:

    def test2(self):
        pass

class TestInterpreter:

    pass
