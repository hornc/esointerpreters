# Conedy eso-interpreter

The specification for this 2 dimensional esoteric tarpit programming language can be found here: https://esolangs.org/wiki/Conedy

This Python interpreter requires [mpmath](https://mpmath.org/) for arbitrarily precision rational instruction pointer coordinates.
The default precision is set to 200 decimal places, but can be changed from the command line with the `-p` / `--precision` options.

    ./conedy.py -h

```
usage: conedy.py [-h] [--precision PRECISION] [--debug] source

Interpreter for esolang Conedy
https://esolangs.org/wiki/Conedy

Language by ais523, 2017.
This interpreter by Salpynx, 2024.

positional arguments:
  source                Source file to process

options:
  -h, --help            show this help message and exit
  --precision PRECISION, -p PRECISION
                        Precision (decimal places)
  --debug, -d           Turn on debug output

```

## Status
This is an experimental interpreter created to explore the computational class of Conedy, currently theorised to be more powerful than a push-down automaton, but not neccesarily Turing complete.
It seems possible that it is Turing complete, but not especially obvious. Deciding either way will be interesting.
Reasoning anything about this language is not very intuitive due to the only data storage being the arbitrary precision position of the instruction pointer.

Many things about the interpreter will likely change. It is not guaranteed to be bug free, and the current execution generates a lot of noise output, which may or may not be useful.

## Implementation details
The Digital Differential Analysis (DDA) ray-casting algorithm, used in some 3d games with simple 2d grid layouts, is used by the interpreter to determine exact instruction pointer intersections.
I used the very helpful [video tutorial](https://www.youtube.com/watch?v=NbSee-XM7WA) from [OneLoneProgrammer](https://www.youtube.com/@javidx9) to understand the technique.
Any bugs in this Python code are all mine, and are my fault for not paying proper attention.

## IO
Output is built up bit-by-bit. This interpreter defaults to little-endian bit order, so least significant bits are generated first, and bytes are output when a full 8 bits have been collected.
Currently complete bytes are output one at a time:

    OUTPUT: H

and additionally the complete output of the program is output once (if) the program terminates.

Input is currently requested manually from the operator by entering a '0' or '1' character when prompted to represented a single bit of input.

The implementation details of these IO conventions might change in future. Possibly more options/alternatives will be added.

## TODO:
* Better (i.e. some) overflow indication
* More interesting examples of what this language can do / demonstrate how it can do *anything*
* TC proof / disproof

## Bugs
If you happen to try this for any reason, please let me know if you notice any bugs in this implementation which disagree with the spec.
These could include:
* Casefolding between net / beacon pairs
* Bad maths
* Incorrect IO

## Usage examples
A Hello World to demonstrate this *is* a programming language:

    ./conedy.py examples/hello-world.con

**result:**
```
{....lots of intermediate output....}
Event 101:
  X collision: [102, 1], at net ş
  ip: (102, 1.4999999999999999999999999999999999999999998093429427881670790500325317917361904819542082200119956893423209278925892339305212734160422002914518877325627069599674465627093752441329236011150605911520974) ⤞ Ş @ 205.5, 1.5
Event 102:
  X collision: [103, 1], at net š
  ip: (103, 1.4999999999999999999999999999999999999999999990789514144355897538648914579310927076422908609662415250692865745308820735938672525285799140110698158827660034152655432201097071267832508386527297613099135) ⤞ Š @ 206.5, 1.5
OUTPUT: !
Event 103:
  X collision: [104, 1], at net ţ
  ip: (104, 1.500000000000000000000000000000000000000000000004449510075190387662488447063134817837476855744124437076959968238981246021285665446721836164197730358054270514902098825023624603252254826866411933520242) ⤞ Ţ @ 207.5, 1.5
Event 104:
  X collision: [208, 1], at boundary
  ip: (208, 1.4999999999999999999999999999999999999999999999955074994893005264663763988589604979322093582100386118401708533239271477369627822301214311192399727302737075477558519109664853039626992327773908497307702) ⤞ None
IP has left the playfield at ip: (208, 1.4999999999999999999999999999999999999999999999955074994893005264663763988589604979322093582100386118401708533239271477369627822301214311192399727302737075477558519109664853039626992327773908497307702) ⤞ None!
Hello, World!

```
