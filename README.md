(sorry, i'm bad at english)
# IJKLang
IJKLang is my own toy programming language.<br />
It created on pure Python, without any libs.
## Dependenses
to compile file, you need installed:
* Python 3
* NASM assembler
* gcc's linker (ld)<br />
(All programs need to be added to path)
## How to compile file
To compile file, you need to run "IJKLang.py".<br />
And my compiler includes some flags:
* `-f` input file name
* `-o` output file name (it can optional include .exe or other, but it didnt make sense)
* `-A` compile into assembler file
* `-O` compile into object file
* `-L` save all files (assembler, object and .exe)
* `-D` debug mode (to many debug prints, do not use it please)
* `-H` help<br />
At all, command will look like this:
`py IJKLang.py -f input.ijk -o output.exe -L`
## What is "pycolors.py"?
it's handmade colored console output, yes it's should be a library but i dont want to make it) That why it here.
