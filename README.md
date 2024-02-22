# ACID

Implementing my idea for a programming language

The idea: I want something that looks like DNA sequence, and is Turing complete.

Didn't know about DNA-Sharp before I started designing it. Technically it isn't original but our implementations are different. Something interesting about both of our languages is that you can make both of them look like DNA in when you write them using --- (actually no, mine requires something a bit different, but I can make a mode like that with the recipricols???) but still, differences between both of our languages. There are obviously other DNA languages but mine is unique for following reasons:

TODO: add reasons.

In any case, the idea was to have fun and work on something interesting. I enjoy programming language design and concepts surrounding it. Plus its an excuse to program, which I haven't done in a while.

What is also cool is the mix of paradigms because you are using 2 stacks as opposed to variables. Granted, not quite a Turing machine since there are a lot of nice to have higher level features, but there are some things/algorithms that would force you to approach it more like a turing machine than a regular programming language (give example, is there even one, it seems like the checking of palindromes is an example.).

Didn't want to use ANTLR or other tools, wanted to get this from ground up myself (and as a result have developed some tools).

TODO: get micsie to make a logo
TODO: *~~Can you use return outside of a function?~~  No (at least, you shouldn't be able to, need to test this)

TODO: less than 500 lines of code

TODO: decide if have arg to disable palindrome function names

TODO: explain why my test cases are in files.

TODO: WRITE UNIT TESTS

TODO: mention drawing the DFA and such, then go make a pull request to the other project after I change their code. Or just create my own, see below.

TODO: ~~write my own NFA to DFA converter. Reeeee.
Or I can borrow someone elses?~~  Have done this and have made it create an SLR table as well

TODO: expand on SLR table to allow for better error logging. Best way I can think of to do this is to write intentionally incorrect programs, see the states that errors are thrown on and use this to learn how best to add error conditions to SLR table.

TODO: Incorporate final CFG definition into the code for better error checking. Or is this even necessary?

TODO: Mascot is a mushroom.

TODO: decide on exact root functionality.

TODO: decide on what extra funny run modes to add and implement (eg: visualizer mode, acid num mode). Do we want to allow for REPL?

TODO: color tokens in VSCode?? In General color tokens (maybe in visualizer)

TODO: do we need to 'isempty' functions? Probably not but should review

TODO: utility that inverts code

TODO: swap some opcodes functionalities so that currently related opcodes are closer together 

#### REQUIRES PYTHON 3.10+ (due to switch case)

## Properties

* Stack based - arithmatic operations work in stack based manner (refer to textbook) (its easier)
* Two stacks as this allows for  Simulating a Turing Machine
* Base 4 number system
* Everything is an opcode (codon) made up of Nueclotides
* Any non-nucleotide character is interpreted as a comment (better make sure you type in lower caps!!!)

Datatypes?

* Basically one Datatype (int)
* Can be interpreted as Asci.

Functions

* You define the name
* Name must be a palindrome
* Scope of function is to outer function it finds itself in.
* Name has restrictions (see later)
* put brackets if you want, I don't care and neither does Acid.
* functions can be defined anywhere, don't have to be defined before they are called ~~(? sure about this??)~~
* Return statement always maps to the function in which it appears (ie, the last defined function name).
* The same function can have multiple return statements or none at all
* Name must be of length n*3 (n>= 0)
* can't use same function name in same scope

If any of these decisions do not make sense to you, maybe you should try more psychedelics (although if it doesn't make sense to you, that is likely a good thing.)

## Program Execution

First goes through and checks everything. If single syntax error, it won't run. Why? Because you wouldn't want to use DNA to create an organism without first checkin you aren't creating a monster.

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

You will notice there are no 'and' or 'or' operators, this is intentional. Both can be simulated using either nested if loops (for and) or elif (for or). Since the base comparison operators ('lessthan' 'greaterthan' and 'equals') don't modify the stack, it doesn't make sense to have include 'and' and 'or'.

Alternatively, you can use a function to evaluate complex conditions and call this before loops/if statements. (TODO: example).

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

Note: can't contain those as codons, so the function name: AAT AAA TAA is invalid but
ATA AGA ATA is (even though it contains AAG from [2,4] the check is only at the codon boundary).

Create util program that tells you if function name is problematic or not. Or maybe even generates palindromic funtion names of length n codons.

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

## Things to test

* loops and ifs with empty bodys
* if statements with duplicate end if tags
* if statements with duplicate else (make sure else matches to correct if statement)
* Reciprocol code does the same thing
* If users input funny chars, can this break the input function? (by funny chars I mean non-standard ascii characters)

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
