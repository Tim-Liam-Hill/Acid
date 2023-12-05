# ACID

Implementing my idea for a programming language

The idea: I want something that looks like DNA sequence, and is Turing complete.

Didn't know about DNA-Sharp before I started designing it. Technically it isn't original but our implementations are different. Something interesting about both of our languages is that you can make both of them look like DNA in when you write them using --- (actually no, mine requires something a bit different, but I can make a mode like that with the recipricols???) but still, differences between both of our languages. There are obviously other DNA languages but mine is unique for following reasons:

TODO: add reasons. 

In any case, the idea was to have fun and work on something interesting. I enjoy programming language design and concepts surrounding it. Plus its an excuse to program, which I haven't done in a while. 

TODO: get micsie to make a logo

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
* then function body is up until the return statement.

If any of these decisions do not make sense to you, maybe you should try more psychedelics. If it doesn't make sense to you, that is likely a good thing. 

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




## Opcodes 

| Primary | Redundant | ExplanationDescription                                                                                                                                 |  |
| ------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | - |
| AAA     | TTT       | Function name declarator. Function name is what appears between this tag. You can use either for the start or for the end.                             |  |
| CAA     | GTT       | Function end. Function name appears between these 2 tags. Declares the end of that function.                                                           |  |
| AAC     | TTG       | Prints numerical value stored at S1[0].                                                                                                                |  |
| CAC     | GTG       | Prints ascii char from value stored at S1[0].                                                                                                          |  |
| AAG     | TTC       | Call function with name between this tag. Can use either for start and end.                                                                            |  |
| CAG     | GTA       | Return from function. Different from function end opcode: this is used to leave function prematurely. Function name appears between the two instances. |  |
| AAT     |           | Push value onto S1. Value is predetermined length (see data types).                                                                                    |  |
| CAT     |           | Pop S1. Interpreted as delete from that stack as opposed to pop and use (so C++ stack style pop as opposed to another language))                       |  |
| ACA     |           | Push top of S1 onto S2 then pop S1.                                                                                                                    |  |
| CCA     |           | Push top of S2 onto S1 then pop S2.                                                                                                                    |  |
| ACC     |           | Add top 2 values of S1 and store result in S1. Essentially pops S1 twice and pushes answer onto S1.                                                    |  |
| CCC     |           | Sub top 2 values of S1 and store result in S1. Essentially pops S1 twice and pushes S[0] - S[1] onto S1.                                              |  |
| ACG     |           | Mult top 2 values of S1.                                                                                                                               |  |
| CCG     |           | Divide top 2 values of S1. Pushes remainder onto S2!!                                                                                                  |  |
| ACT     |           | Modulus operator (syntactic sugar to match the pow)                                                                                                    |  |
| CCT     |           | Pow (S[0] ^ S[1]) and push result to S1                                                                                                                |  |
| AGA     |           | Start if statement block                                                                                                                               |  |
| CGA     |           | End if statement block                                                                                                                                 |  |
| AGC     |           | Else if                                                                                                                                                |  |
| CGC     |           | Else                                                                                                                                                   |  |
| AGG     |           | Equals S1 (doesn't remove). Treats both items as numbers.                                                                                              |  |
| CGG     |           | Not Equals S1 (doesn't remove)                                                                                                                         |  |
| AGT     |           | Less than                                                                                                                                              |  |
| CGT     |           | Greater than                                                                                                                                           |  |
| ATA     |           | And                                                                                                                                                    |  |
| CTA     |           | Or                                                                                                                                                     |  |
| ATC     |           | Not                                                                                                                                                    |  |
| CTC     |           | Push user input onto S1                                                                                                                                |  |
| ATG     |           | Start while loop                                                                                                                                       |  |
| CTG     |           | End while loop                                                                                                                                         |  |
| ATT     |           | Swap S1 and S2 top values.                                                                                                                             |  |
| CTT     |           | Swap S2 and S1 top values. Yeah, this is the same as the above I know. Deal with it.                                                                   |  |


## Questions

*Can you define nested functions?* 

We can do it, it will just be effort. Will need a scope table. Nested functions would only be accessible within their scope though because otherwise that is just effort. 

*What is function scope?* 

Functions are just glorified labels really. 

*Can we make the DNA look cool like the other example?* 

I hope so. 

*How are we going to handle nested while loops?*

Match to nearest and while, doesn't have the same issue that functions have due to unique names (lack thereof)
