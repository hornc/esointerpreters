## Thue-Mirr interpreter,
https://esolangs.org/wiki/Thue-Mirr

```
usage: thue-mirr.py [-h] [--debug] [--char] [--num NUM] file

Thue-Mirr https://esolangs.org/wiki/Thue-Mirr Interpreter v1.0 by Salpynx. 2019 CC0

positional arguments:
  file               source file to process

optional arguments:
  -h, --help         show this help message and exit
  --debug, -d        turn on debug output
  --char, -c         character output for valid Unicode codepoints, number
                     otherwise
  --num NUM, -n NUM  number of output lines to return (code does not terminate
                     naturally. Set to 0 for experimental auto-terminate on
                     no-output fn.)
```

Example usage for the included examples:

#### Hello World:

    ./thue-mirr.py --char -n12 examples/hello-world.tm

### A "Stretching-the-Truth"-machine in Thue-Mirr

```
/ *\0
 \/ 
```
All numbers in this program are 3 bit little-endian 'words'

Hence `*` is either '' for zero, or `10` for 1

* `0` = `b0`
* `1` = `b100`

Let's pretend the `\` marks the most significant bit.

Explicitly:

The zero program:
```
/ \0
 \/
```

The one program:
```
/ 10\0
 \/
```

Output is in 3-bit little-endian 'words'.

* Input b`\0`    > `000` (then infinte loop with no output. Since the language has no halt, assume loop with no possibility of output is halt.)
* Input b`10\0`  > `100` repeating

      # Run the included 0 input version:
      ./thue-mirr.py -n0 examples/truth-machine0.tm

      # Run the included 1 input version:
      ./thue-mirr.py -n0 examples/truth-machine1.tm

      # for the first 4 cycles of truth-machine1:
      ./thue-mirr.py -n12 examples/truth-machine1.tm
