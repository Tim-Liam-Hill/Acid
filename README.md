# ACID

![Acid Mascot](Acid_mascot.gif)

## Welcome

What you are currently looking at is an esoteric programming language designed and implemented by yours truly. This programming language is a Turing Complete, Interpreted programming language inspired by DNA. Please note that while the main functionality has been implemented, this project is still a work in progress and so both unit tests and this README are not yet finalized. Read on to find out what further plans I have in store.

## The Idea

I had often heard people compare Human-written computer code to DNA and this irked me somewhat since, although the comparison is apt in some ways, it is often used in certain dubious philosophical arguments. Still, it got me thinking about how to create a programming language that better represented DNA and some of its qualities. The result is Acid.

I should note that even before doing further research I did not expect to be the first person to implement a programming language based on DNA. That being said, I do believe Acid has some unique properties that set it apart from the other projects I have found based on DNA ([DNA-Sharp](https://esolangs.org/wiki/DNA-Sharp) and [RNA](https://esolangs.org/wiki/RNA#DNA) are 2 other esoteric languages inspired by DNA are compared with Acid in a section later in this README if you are interested).

In any case, the idea was to have fun and work on something interesting. I enjoy programming language design and the concepts surrounding it and wanted to have a programming language, even a simple one, that I can say I developed and implemented from the ground up without the use of [ANTLR](https://www.antlr.org/) or other related tools (I don't count the work I did during my undergraduate studies since the compiler implemented in my course was for a language I did not design). As a result of this choice, I ended up developing a suite of tools to assist in Context Free Grammar operations, DFA/NFA operations and the creation of an [SLR parse table](https://www.geeksforgeeks.org/slr-parser-with-examples/) which is now [a separate project](https://github.com/Tim-Liam-Hill/CFGNullableFirstFollow) that I will continue working on.

## Requirements

Running the interpreter requires Python version 3.10+ due to the presence of the 'match' statement. Python 3.12.0 is the recommended version to use, but other versions should be suitable as wel.

## Properties

Acid is a stack based programming language with 2 stacks (s1 and s2) that are manipulated by the user via opcodes. It has no variables: all data input, manipulation and output is done via the stacks. There are only 4 symbols that are recognized by acid: A, C, G and T (corresponding to the four nucleotides that make up DNA). Any non-nucleotide character is interpreted as a character (and I highly recommend keeping all of your comments in lowercase to avoid accidentally adding an extra nucleotide to your code, unless you like mutations in DNA).

Each opcode consists of 3 nucleotides since in DNA, a single amino acid is also comprised of 3 nucleotides. Similarly to DNA, sequences of amino acids (opcodes) are combined to form proteins which, in the context of Acid, can be thought of as units of functionality in your program (in an abstract sense). However, there are only 32  unique operations and so for any specific operation (eg: push a number onto stack 1) there are exactly 2 opcodes that achieve this functionality. This is intentional since in human DNA, various different combinations of nucleotides can form the same amino acid.

#### Data Types

As for data types, there is only one data type: the Number data type. Numbers are all integers and are specified by a base 4 number system in the Acid code, with symbols mapping to the following digits:

* A = 0
* C = 1
* G = 2
* T = 3

Numbers are written in Sign-Magnitude notation and by default, a number is 5 Codons in length (giving a range of [-268435455, 268435455] inclusive).

Writing numbers work as follows:

* If the leading nucleotide is an 'A', the number is positive
* If the leading nucleotide is a 'C', the number is negative
* If the leading nucleotide is a 'G', the number is positive AND its magnitude MAX_VALUE - magnitude.
* If the leading nucleotide is a 'T', the number is negative AND its magnitude MAX_VALUE - magnitude.

Does this sound confusing? If so, let try and give some examples:

*Example 1*

```
AAA AAA AAA AAA AAG 
Written in base 4 notation this becomes:
+00000000000002
The integer value for this would be:
2*(pow(4,0)) = 2
```

*Example 2*

```
CAA AGA ATA AAA ACA 
Written in base 4 notation this becomes:
-00020030000020
The integer value for this would be:
-1*(1*(pow(4,1)) + 3*(pow(4,7))+2*(pow(4,10)))= -2146308
```

*Example 3*

```

TAA GTT AAA ACC AAA 
Written in base 4 notation this becomes:
+00233000011000
The integer value for this would be: 
268435455 - (1*(pow(4,3)) + 1*(pow(4,4)) + 3*(pow(4,9))+ 3*(pow(4,10)) +   2*(pow(4,11))) = 256114367
```

Because the impemented in this way, you can 'invert' all nucleotides of a number and have it still represent the same number. That is to say: we define the inverse of a nucleotide to be the nucleotide that would bond with this symbol in a strand of DNA. See below for an example:

```
AAAAAAAAACAACGG = 1050
TTTTTTTTTGTTGCC = 1050
```

To assist with writing numbers in Acid I have included a helper 'Bas4Convert.py' file in the source code.

#### IO

Now you may be thinking "if the only data type available is integer numbers, then you can't print and handle strings" but that isn't the case. While everything is treated as a number during stack operations, the input and output operations have the following behaviours:

* Read User Input (opcodes ``CTC`` and ``GAG``)

Acid will first try and interpret the input as an integer number. If successful, this number is pushed on top of stack 1. If the input cannot be interpreted as a number, the ascii value for each character making up the input string is pushed onto stack 1.

* Print as number (opcodes ``AAC`` and ``TTG``)

Acid will print the top value of stack 1 as an integer number

* Print as char (opcodes ``CAC`` and ``GTG``)

Acid will interpret the top value of stack 1 as the integer code for an ascii value and print the corresponding ascii char. For example: if the number on top of stack 1 is 97 then the character 'a' will be output.

#### Functions

*Wow, this language sounds a lot like a [Turing-Tarpit](https://esolangs.org/wiki/Turing_tarpit)...*  hold that thought. There are some cool features to this language that help make it (slightly) more convenient than an actual Turing machine. An example of this are functions - yes, that's right, you can define functions in this programming language! Functions are defined by having a pair of 'start-function' tags and matching 'end-function' tags both with the same associated function name (the function body is the contents that appears between these tags). You can define functions within functions, and the scope of these functions is tied to the previous function it was declared in. Just keep in mind the following: function names can't contain the below certain codons:

* AAA
* TTT
* CAA
* GTT
* AAG
* TTC
* CAG
* GTA

Note: the check is at the codon boundary so the function name ``AAT AAA TAA`` is invalid (contains AAA) but ``ATA AGA ATA`` is valid since even though it contains AAG from [2,4], the check is only on a codon-by-codon basis.

Furthermore, all function names must be palindromes (for no other reason than I think this should be the case). If this decision does not make sense to you, this is likely a good thing. Below is an example of a program that defines an empty function:

```
AAA CAT TAC AAA #define function with name 'cattact' between 2 'start function' codons/tags
#empty function body
CAA CAT TAC CAA #declare that the body of funciton 'cattac'is now finished
```

*You didn't hear this from me, but the empty string is a valid function name. Do with this information what you will.*

## Opcodes

Below is the table that maps opcodes to their corresponding actions.

| Primary | Redundant | ExplanationDescription                                                                                                                                                        |  |
| ------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | - |
| AAA     | TTT       | Function name declarator. Function name is what appears between this tag. You can use either for the start or for the end.                                                    |  |
| CAA     | GTT       | Function end. Function name appears between these 2 tags. Declares the end of that function and is an implicit return statement.                                              |  |
| AAC     | TTG       | Prints numerical value stored at S1[0].                                                                                                                                       |  |
| CAC     | GTG       | Prints ascii char from value stored at S1[0].                                                                                                                                 |  |
| AAG     | TTC       | Call function with name between this tag. Can use either 'AAG' or 'TTC' for start/end.                                                                                        |  |
| CAG     | GTA       | Return from function. Different from function end opcode: this is used to leave function prematurely. Function name appears between the two instances.                        |  |
| AAT     | TTA       | Push value onto S1. Value is predetermined length (see data types).                                                                                                           |  |
| CAT     | GTA       | Pop S1. Interpreted as delete from that stack as opposed to pop and use (so C++ stack style pop as opposed to another language))                                              |  |
| ACA     | TGT       | Push top of S1 onto S2 then pop S1. Basically, move S1 to S2                                                                                                                  |  |
| CCA     | GGT       | Push top of S2 onto S1 then pop S2. Basically, move S2 to S1                                                                                                                 |  |
| ACC     | TGG       | Add top 2 values of S1 and store result in S1. Follows Postfix notation                                                                                                       |  |
| CCC     | GGG       | Sub top 2 values of S1 and store result in S1. Follows Postfix notation                                                                                                      |  |
| ACG     | TGC       | Mult top 2 values of S1.                                                                                                                                                      |  |
| CCG     | GGC       | Divide top 2 values of S1. Pushes remainder onto S2!! (Number that is popped first is dividend, second number is divisor )                                                   |  |
| ACT     | TGA       | Root operation. S[0] to the root of S[1])). Pushes int diff onto S2 (todo: elaborate))                                                                                        |  |
| CCT     | GGA       | Pow (S[0] ^ S[1]) and push result to S1                                                                                                                                       |  |
| AGA     | TCT       | Start if statement block                                                                                                                                                      |  |
| CGA     | GCT       | End if statement block                                                                                                                                                        |  |
| AGC     | TCG       | Else if                                                                                                                                                                       |  |
| CGC     | GCG       | Else                                                                                                                                                                          |  |
| AGG     | TCC       | Equals S1 (doesn't remove). Treats both items as numbers.                                                                                                                     |  |
| CGG     | GCC       | Check if S1 is empty. IS a boolean returning function Allows for more convenient operations (TODO: elaborate with an example)                                                 |  |
| AGT     | TCA       | Less than (is second last element s1 smaller than last element)                                                                                                               |  |
| CGT     | GCA       | Greater than (is second last element s1 greater than last element)                                                                                                          |  |
| ATA     | TAT       | Swap first and last elements of s1                                                                                                                                            |  |
| CTA     | GAT       | Check if s2 empty. IS A BOOLEAN RETURNING FUNCTION                                                                                                                            |  |
| ATC     | TAG       | Not                                                                                                                                                                           |  |
| CTC     | GAG       | Push user input onto S1. If input is an integer within the range of the program, it will push a single int onto s1 otherwise it will push the ascii code of each char onto s1 |  |
| ATG     | TAC       | Start while loop                                                                                                                                                              |  |
| CTG     | GAC       | End while loop                                                                                                                                                                |  |
| ATT     | TAA       | Swap S1 and S2 top values.                                                                                                                                                    |  |
| CTT     | GAA       | Copy top of S1 and push that value back onto S1. Without this, some things become very difficult/impossible (eg, how do you retain a number after an operation?) )            |  |

## Proof of Turing Completeness

The [formal definition for a Turing Machine](https://brilliant.org/wiki/turing-machines/) is as follows:

A Turing Machine is defined as the 7-tuple **⟨**Q**,**q**0****,**F**,**Γ**,**b**,**Σ**,**δ**⟩**, where

* **Q** is a finite, non-empty set of *states*
* **q**0∈**Q** is the *initial state*
* **F**⊂**Q** is the set of *accepting states*
* **Γ** is a finite, non-empty set of *tape symbols*
* **b**∈**Γ** is the *blank symbol*
* **Σ**⊂**Γ**∖**{**b**}** is a set of *input symbols*
* **δ**:**(**Q**∖**F**)**×**Γ**→**Q**×**Γ**×**{**L**,**R**}** is the  *transition function* , which is a partial function

Suppose you have some Turing Machine T. This can be simulated by Acid in the following manner:

* Create a new, empty Acid program
* Select some symbol **s** such that **s** is not an element of **Γ** (**Γ** \ {**s**} == **Γ**)

Now we need to stop here for a moment, since this may seem more complicated than it needs to be. Since **Γ** is  a finite set, we can ensure that there is a one to one mapping from numbers (our only data type) in the range allowed by our number of codons used to represent numbers to the symbols. Then, we select some other arbitrary number that hasn't been used to serve as the empty symbol. 

*But what if we have more symbols than numbers? How do we deal with that?* I am glad you asked. In this case, we can increase the number of codons used to represent numbers to increase the range as required. Since we are more concerned with theoretical possibility and not constrained by silly things like machine memory, this is completely fine.

One other thing to note, we have two different representations for 0 and so if you wanted/if it is more convenient, just use one of those instead. 

* For each state in **Q**, create a new function in an Acid program.
* For each created function, in the function body, create *n* many 'if' statements where *n* is the cardinality of **Γ**. The body of each 'if' statement is the 'return' function for now, and each if statement checks for equality between the top of S1 and one symbol of **Γ**.

That is to say, the body of each function would resemble the pseudo-code below:

```

func state1(){
	if(S1_top == symbol_1){
		return
	}
	if(S1_top == symbol_2){
		return
	}
	...
	if(S1_top == symbol_n){
		return
	}
}
//repeat for each other state
```

* For each function that does NOT map to a state in **F** , and each **e** ∈ **Γ**, add the following to the contents of the if statement that checks for equality with symbol **e**

```
popS1()
pushS1(x)
```

Where *x* is the element of **Q** that would be written onto the tape when in state corresponding to the function's name and symbol *e* is read.

Then, to simulate left transition:

```
movS1S2() 
```

That is, run the opcode that copies the top of S1 to S2 and pops of S1 as this simulates moving the tape to the left. Similarly, a right transition would be the below command:

```
movS2S1()
```

Finally, call the function with the name of the state that is the new state/state to be transitioned to. 

* For all functions *f*  ∈  F, add a single *return* statement to the function body 

The only potential issue in this particular configurations is if any state does not have a well defined transition for some symbol in the alphabet. In such cases, the body of the corresponding if statement can be an infinite loop.

TODO: Give an example of a Turing machine as an Acid Program


# README BEYOND THIS POINT IS STILL IN PROGRESS

What is also cool is the mix of paradigms because you are using 2 stacks as opposed to variables. Granted, not quite a Turing machine since there are a lot of nice to have higher level features, but there are some things/algorithms that would force you to approach it more like a turing machine than a regular programming language (give example, is there even one, it seems like the checking of palindromes is an example.).

## Program Execution

First goes through and checks everything. If single syntax error, it won't run. Why? Because you wouldn't want to use DNA to create an organism without first checkin you aren't creating a monster.

## How Acid reflects DNA

* Inversion of codons = same thing (like DNA sorta)
* Redundancy
* Nuecleotides->Codons->Proteins
* invert entire code (incl numbers) and you get same program (DNA both sides replication thingy)
* It can look like DNA
* R

## Visualisation

If we want the visualisation to come out nicely then the recipricol needs to be the redundant for each opcode. We may also need to do some magic with our number system. My visualisation is different to other languages in this way: lets say our program is 'AAC CAA GTG ACA'. This represents one side of the DNA sequence, so to do

AA

C-C

A--A

Doesn't make sense (in real life DNA, A-A is invalid). Instead there would be a reciprocal side; the complement:

AT

A-T

C--G and so on.

That's how my visualisation will work.

TODO: implement and make it look like the code is rotating.

## Boolean Statements

* 0 is False
* Non-0 is True.
* Actually no, there is no explicit true and false
* You have to explicitly compare two different values.

You will notice there are no 'and' or 'or' operators, this is intentional. Both can be simulated using either nested if loops (for and) or elif (for or). Since the base comparison operators ('lessthan' 'greaterthan' and 'equals') don't modify the stack, it doesn't make sense to have include 'and' and 'or'.

Alternatively, you can use a function to evaluate complex conditions and call this before loops/if statements. (TODO: example).

## Comments

* Any non A C G T characters interpreted as comments
* so don't accidentally use those in your comments
* Fun way if introducing mutation to code

## TODOs

~~TODO: get micsie to make a logo~~
TODO: *~~Can you use return outside of a function?~~  No (at least, you shouldn't be able to, need to test this)

TODO: less than 500 lines of code

TODO: release CFG once finalized (and the work is more polished)

TODO: decide if have arg to disable palindrome function names

~~TODO: explain why my test cases are in files.~~

TODO: WRITE UNIT TESTS

TODO: publish as a Python module. Can include utilities as separate sub commands to make writing Acid programs easier.

TODO: mention drawing the DFA and such, then go make a pull request to the other project after I change their code. Or just create my own, see below.

TODO: ~~write my own NFA to DFA converter. Reeeee.
Or I can borrow someone elses?~~  Have done this and have made it create an SLR table as well

TODO: expand on SLR table to allow for better error logging. Best way I can think of to do this is to write intentionally incorrect programs, see the states that errors are thrown on and use this to learn how best to add error conditions to SLR table. Otherwise, the CFG itself can encode error messages I suppose (via non-terminals that represent specific cases of syntactic errors. I believe this is how the Python implementation does it, see [here](https://github.com/python/cpython/blob/main/Grammar/python.gram#L1187) )

TODO: Incorporate final CFG definition into the code for better error checking. Or is this even necessary?

*~~TODO: Mascot is a mushroom.~~ *

TODO: decide on what extra funny run modes to add and implement (eg: visualizer mode, acid num mode). Do we want to allow for REPL?

TODO: color tokens in VSCode?? In General color tokens (maybe in visualizer)

TODO: do we need to 'isempty' functions? Probably not but should review

TODO: utility that inverts code

TODO: swap some opcodes functionalities so that currently related opcodes are closer together

TODO: change some logging statements from debug to info for easier debugging (getting bogged down in all the debug statements when searching for small things)

TODO: make a helper function that, given some integer x >= 0 generates all valid function names of length x codons.

##### Replacing bools

The opcodes for 'and' and 'or' are now free for something else, but I am not sure what exactly I want to replace them with. Some things that come to mind:

* size of stacks

Problem is, we need to store these results on the stack so to get len(s1) we actually add to that length. In any case, the user can keep track of this and would still need to keep track of their own lengths anyway

* some sort of reversal

I don't like the idea of just directly reversing the stacks, it seems a bit too high level for what the language actually wants. Maybe something smaller like 'take top of s1 and move it to back'? Still, we want something that has use (this has use in reversing strings but still).

A nice idea for this could be to swap first and last elements of s1, this is convenient for palindrome checking. Also useful for sorting lists. What is the reciprocol of this though?

Maybe we could have a generalized version (swap top of s1 based on an offset?). Allows for some sort of random access I suppose

* push marker and check if marker?

this could have some uses with respect to a user keeping track of strings without having to know string length, but it introduces complexity in all other operations (everything will need to have a check to see if it is operating on a marker and handle accordingly). Again, this is something the end user can implement in other ways.

* increment and decrement

Nice to have but not necessary. I want opcodes that significantly open up more possibilities/make bigger things less tedious.

* check if s2 empty

matches the check if s1 is empty operation we currently have

Maybe lets get back to this once I have written some more sample programs.

## Tips

* With functions, have the function return the stack to the state it was before it was called (similar to assembly) if returning nothing. Else, always have return type be top of one stack (possibly S2).
* If you are tired of trying to always think up new function names, you can generate an infinite number of valid function names using the pattern /CAT (TAT)* TAC/. Proof of this is left as an exercise to the reader.

## Questions

*Can you define nested functions?*

We can do it, it will just be effort. Will need a scope table. Nested functions would only be accessible within their scope though because otherwise that is just effort.

*What is function scope?*

Functions are just glorified labels really.

*Can we make the DNA look cool like the other example?*

I hope so.

*How are we going to handle nested while loops?*

Match to nearest and while, doesn't have the same issue that functions have due to unique names (lack thereof)

*Add a boolean maybe?  Value for true since we have an opcode left over?*

Eh, maybe we can make it just a function that returns true. Still, don't really need it.

*Write a quine?*

If we can.

*Can you use return outside of a function?*

## Compared to other similar Languages

TODO: compare to [DNA-Sharp](https://esolangs.org/wiki/DNA-Sharp) and [RNA](https://esolangs.org/wiki/RNA#DNA)

## Next Steps

In future might expand on this and make a programming language that can be improved via random mutation and descent with modification. Still, far from that for now.

Website with interpreter for web use.

VScode highighter.

## Things to test

* loops and ifs with empty bodys
* if statements with duplicate end if tags
* if statements with duplicate else (make sure else matches to correct if statement)
* Reciprocol code does the same thing
* If users input funny chars, can this break the input function? (by funny chars I mean non-standard ascii characters)
* Run multiple programs/ASTs one after the other and verify that they produce the correct input

## Things I have learned

* Still trying to wrap my head around SLR parsing
* My understanding is that we have a CFG that describes the grammar of our language
* We then need to get this into an unambiguous format
* Once we do that, it essentially becomes almost regular, and we can use a stack and a DFA to determine how the tokens we have in our output language were generated according the the rules of the CFG
* Essentially, we work beackwards. The reason we need unambiguity is because of the meaning we impose on the symbols within the CFG (eg, CFG doesn't necessarily adhere to rules of precedence we want to apply to our language)
* Wild
* We are kind of going back and forth on the DFA since we remember previous states
* So I think it is a thing of the DFA current State tells us what could be next (since it knows how for each rule things can go together and is a combination of all rules)

With the reduce, the psuedo code is kinda bad. Basically: pop off everything then BEFORE adding non-terminal to stack, copy the top of the stack into temp variable. Use that as state for cross referencing table.

## Fixing Conflicts

Shift reduce conflict means that we have ambiguity: we could either reduce to a certain non-terminal OR we could continue taking in symbols for a longer non-terminal. That means that there is an overlap in either first or follow for one of our productions.

## Thoughts for later

* definitely worth it to generate tools for the manual operations (DFA, Follow, First etc) since it is fun to play around with to learn more and saves a lot of time in the long run
* will I reuse those tools though? Probably
* Turing Tarpits are very easy to fall into
* Designing a grammar is not always trivial, need to be careful about whether or not your grammar is the correct or allows more (or less) than what you actually want
* Ideas about how to store data: in terms of "how do I avoid making this an absolute mess of dictionaries?" (answer: you didn't avoid that at first, but maybe later)
* Interesting how useful DFAs can really be. Also interesting how large a table can end up being for seemingly small grammars
* Requiring function names to be defined before use makes for easier implementation but makes it more tedious to write programs in the language, so it is something I wanted to avoid.
* Using stack based language model and Postfix notation is great if you don't want to use brackets, but in a sense my function definition tags are glorified brackets in a way
* What is the remainder for a root operation anyway?? Is it useful in general to know this in the same way that it is useful to know remainder for division? Doesn't seem like it

For division, the remainder is easy to relate back to the input arguments since it is the fraction of the divisor that fits into the remaining integer amount of the dividend (if I have those terms right). In other words, the fractional part of the answer from a division can easily be separated from the integer part. The same cannot be said for roots: in each iteration of multiplication the fractional component (<1) MUST be incorporated into the equation. Just using it by itself (eg, raising it to the same power) is not the same as when you multiply the remainder/fractional part of your answer from division. Never really thought about this before and it is hard to put into words, so Ill have to expand on this another time.
