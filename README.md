# ACID

Implementing my idea for a programming language

The idea: I want something that looks like DNA sequence, and is Turing complete.

Didn't know about DNA-Sharp before I started designing it. Technically it isn't original but our implementations are different. Something interesting about both of our languages is that you can make both of them look like DNA in when you write them using --- (actually no, mine requires something a bit different, but I can make a mode like that with the recipricols???) but still, differences between both of our languages. There are obviously other DNA languages but mine is unique for following reasons:

TODO: add reasons.

In any case, the idea was to have fun and work on something interesting. I enjoy programming language design and concepts surrounding it. Plus its an excuse to program, which I haven't done in a while.

What is also cool is the mix of paradigms because you are using 2 stacks as opposed to variables. Granted, not quite a Turing machine since there are a lot of nice to have higher level features, but there are some things/algorithms that would force you to approach it more like a turing machine than a regular programming language (give example, is there even one??).

Didn't want to use ANTLR or other tools, wanted to get this from ground up myself 

TODO: get micsie to make a logo
TODO: *Can you use return outside of a function?*

## Properties

* Stack based - arithmatic operations work in stack based manner (refer to textbook) (its easier)
* Two stacks as this allows for  Simulating a Turing Machine
* Base 4 number system
* Everything is an opcode (codon) made up of Nueclotides
* Any non-nucleotide character is interpreted as a comment (better make sure you type in lower caps!!!)

Datatypes?

* Basically one Datatype
* Can be interpreted as Asci.

Functions

* You define the name
* Name must be a palindrome
* Scope of function is to outer function it finds itself in.
* Name has restrictions (see later)
* put brackets if you want, I don't care and neither does acid.
* functions can be defined anywhere, don't have to be defined before they are called (? sure about this??)
* Return statement always maps to the function in which in appears.

If any of these decisions do not make sense to you, maybe you should try more psychedelics. If it doesn't make sense to you, that is likely a good thing.

## Program Execution

First goes through and checks everything. If single syntax error, it won't run. Why? Because you wouldn't want to use DNA to create an organism without first checkin you aren't creating a monster.

## Visualisation

If we want the visualisation to come out nicely then the recipricol needs to be the redundant for each opcode. We may also need to do some magic with our number system. My visualisation is different in this way: lets say our program is 'AAC CAA GTG ACA'. This represents one side of the DNA sequence, so to do

AA

C-C

A--A

Doesn't make sense. Instead there would be a reciprocal side: the complement:

AT

A-T

C--G and so on.

That's how my visualisation will work.

## Numbers

* numbers are 5 codons long
* sign and magnitude
* A leading symbol means positive
  C leading symbol means negative
  T leading symbol means positive AND recipricol interpretation
  G leading symbol means negative AND recipricol interpretation

TODO: test the recipricol with negative numbers. Should work but you never know.

## Boolean Statements

* 0 is False
* Non-0 is True.
* Actually no, there is no explicit true and false
* You have to explicitly compare two different values.

## Comments

* Any non A C G T characters interpreted as comments
* so don't accidentally use those in your comments
* Fun way if introducing mutation to code

## Opcodes

I realize that I may want an opcode for checking if S1 is empty. Could make things a bit easier (eg: lets you determine length of string without having to keep a count as you take in every char from user).

TODO: determine the strings from which valid function names can be derived.

Can't contain:

* AAA
* TTT
* CAA
* GTT
* AAG
* TTC
* CAG
* GTA

Create util program that tells you if function name is problematic or not. Or maybe even generates palindromic funtion names of length n codons. 

| Primary | Redundant | ExplanationDescription                                                                                                                                             |  |
| ------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | - |
| AAA     | TTT       | Function name declarator. Function name is what appears between this tag. You can use either for the start or for the end.                                         |  |
| CAA     | GTT       | Function end. Function name appears between these 2 tags. Declares the end of that function and is an implicit return statement.                                  |  |
| AAC     | TTG       | Prints numerical value stored at S1[0].                                                                                                                            |  |
| CAC     | GTG       | Prints ascii char from value stored at S1[0].                                                                                                                      |  |
| AAG     | TTC       | Call function with name between this tag. Can use either for start and end.                                                                                        |  |
| CAG     | GTA       | Return from function. Different from function end opcode: this is used to leave function prematurely. Function name appears between the two instances.             |  |
| AAT     | TTA       | Push value onto S1. Value is predetermined length (see data types).                                                                                                |  |
| CAT     | GTA       | Pop S1. Interpreted as delete from that stack as opposed to pop and use (so C++ stack style pop as opposed to another language))                                   |  |
| ACA     | TGT       | Push top of S1 onto S2 then pop S1. Basically, move S1 to S2                                                                                                       |  |
| CCA     | GGT       | Push top of S2 onto S1 then pop S2. Basically, move S2 to S1                                                                                                      |  |
| ACC     | TGG       | Add top 2 values of S1 and store result in S1. Essentially pops S1 twice and pushes answer onto S1.                                                                |  |
| CCC     | GGG       | Sub top 2 values of S1 and store result in S1. Essentially pops S1 twice and pushes S[0] - S[1] onto S1.                                                          |  |
| ACG     | TGC       | Mult top 2 values of S1.                                                                                                                                           |  |
| CCG     | GGC       | Divide top 2 values of S1. Pushes remainder onto S2!!                                                                                                              |  |
| ACT     | TGA       | Root operation. S[0] to the root of S[1]))                                                                                                                         |  |
| CCT     | GGA       | Pow (S[0] ^ S[1]) and push result to S1                                                                                                                            |  |
| AGA     | TCT       | Start if statement block                                                                                                                                           |  |
| CGA     | GCT       | End if statement block                                                                                                                                             |  |
| AGC     | TCG       | Else if                                                                                                                                                            |  |
| CGC     | GCG       | Else                                                                                                                                                               |  |
| AGG     | TCC       | Equals S1 (doesn't remove). Treats both items as numbers.                                                                                                          |  |
| CGG     | GCC       | Check if S1 is empty. Allows for more convenient operations(Original) -> Not Equals S1 (doesn't remove)                                                            |  |
| AGT     | TCA       | Less than                                                                                                                                                          |  |
| CGT     | GCA       | Greater than                                                                                                                                                       |  |
| ATA     | TAT       | And                                                                                                                                                                |  |
| CTA     | GAT       | Or                                                                                                                                                                 |  |
| ATC     | TAG       | Not                                                                                                                                                                |  |
| CTC     | GAG       | Push user input onto S1                                                                                                                                            |  |
| ATG     | TAC       | Start while loop                                                                                                                                                   |  |
| CTG     | GAC       | End while loop                                                                                                                                                     |  |
| ATT     | TAA       | Swap S1 and S2 top values.                                                                                                                                         |  |
| CTT     | GAA       | Copy top of S1 and push that value back onto S1. Without this, some things become very difficult/impossible (eg, how do you retain a number after an operation?) ) |  |

## Tips

With functions, have the function return the stack to the state it was before it was called (similar to assembly) if returning nothing. Else, always have return type be top of one stack (possibly S2).

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

## Next Steps

In future might expand on this and make a programming language that can be improved via random mutation and descent with modification. Still, far from that for now. 


Website with interpreter for web use. 


VScode highighter.
