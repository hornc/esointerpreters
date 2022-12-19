#!/usr/bin/env python3

desc = """
    Thue-Mirr https://esolangs.org/wiki/Thue-Mirr
    Interpreter v1.0 by Salpynx. 2019 CC0
"""

import argparse

class ThueMirrField():
    unit_field = [] # the original source code unit tile which is repeated infinitely
    unit_w = 0
    gx = gy = 0     # global x,y coords of the current code tile
    x = y = 0       # x,y coords within the current tile
    facing = [1, 0]
    hits = {}       # dict to store flip counts of every mirror that gets hit, key = current_key() 'hash'
    lines_output = 0
    max_output = None
    last_output = 0 # cycles since last output
    max_nooutput = None

    def __init__(self, source_file, max_output=None):
        with open(source_file, 'r') as f:
            for line in f:
                line = line.strip("\n")
                if len(line) > self.unit_w:
                    self.unit_w = len(line)
                self.unit_field.append(line)
        self.max_output = max_output
        self.unit_h = len(self.unit_field)
        if max_output == 0: # experimental feature: set max_output to zero to auto terminate if a threshold f(h, w) of cycles pass without any output.
            GRID_SIZE_FACTOR = 2 # has to be greater than 1.875 Have found 15 cycles between output from a 4x2 grid.
            self.max_output = None
            self.max_nooutput = self.unit_h * self.unit_w * GRID_SIZE_FACTOR 
            if DEBUG:
                print("Current GRID_SIZE_FACTOR: ", GRID_SIZE_FACTOR)
                print("Max cycles to allow without output: ", self.max_nooutput)

    def active(self):
        """Returns False on interpreter specific halt conditions, True otherwise.""" 
        return (self.max_output is None and self.max_nooutput is None) or \
               (self.max_output and self.lines_output < self.max_output) or \
               (self.max_nooutput and self.last_output < self.max_nooutput)

    def current_key(self):
        """Returns a unique key for the current command mirror.
           Currently str 'x|y', but could be any hash."""
        return "%d|%d" % (self.gx * self.unit_w + self.x, self.gy * self.unit_h + self.y)

    def mirror_flipped(self):
        """Check if we have a hit count for this mirror, returns Truthy if mirror is flipped from original."""
        hits = self.hits.get(self.current_key(), 0)
        return bin(hits).count('1') & 1

    def get_command(self):
        try:
            c = self.unit_field[self.y][self.x]
        except IndexError:  # source lines don't have to be unit_w long, this in effect fills them with ' '
            c = ' '
        if c in '\\/':
            if self.mirror_flipped():
                c = chr((~ord(c) & 17) * 3 + 44)
            try:
                self.hits[self.current_key()] += 1
            except KeyError:
                self.hits[self.current_key()] = 1
        self.process(c)
        return c

    def process(self, c):
        self.last_output += 1
        if c == '\\':
            self.facing = self.facing[::-1]
        if c == '/':
            self.facing = self.facing[::-1]
            self.facing[0] = -self.facing[0]
            self.facing[1] = -self.facing[1]
        if c == 'x':
            self.tm_print(self.gx * self.unit_w + self.x)
        if c == 'y':
            self.tm_print(self.gy * self.unit_h + self.y)
        if c in '0123456789':
            self.tm_print(c, num=True)

    def tm_print(self, c, num=False):
        """All program output goes though here."""
        self.last_output = 0 # reset last output counter
        if CHAR and not num:
            try:
                print(chr(c), end='')
                if c == 10: # newline
                    self.lines_output += 1
                return
            except ValueError:
                pass 
        print(c)
        self.lines_output += 1

    def advance(self):
        self.x += self.facing[0]
        self.y += self.facing[1]
        if self.y >= self.unit_h:
            self.y = 0
            self.gy += 1
        if self.x >= self.unit_w:
            self.x = 0
            self.gx += 1
        if self.y < 0:
            self.y = self.unit_h - 1
            self.gy -= 1
        if self.x < 0:
            self.x = self.unit_w - 1
            self.gx -= 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=desc, allow_abbrev=True)
    parser.add_argument('--debug', '-d', help='turn on debug output', action='store_true')
    parser.add_argument('--char', '-c', help='character output for valid Unicode codepoints, number otherwise', action='store_true')
    parser.add_argument('--num', '-n', help='number of output lines to return (code does not terminate naturally. Set to 0 for experimental auto-terminate on no-output fn.)', type=int)
    parser.add_argument('file', help='source file to process')
    args = parser.parse_args()

    DEBUG = args.debug
    CHAR = args.char
    source_file = args.file
    f = ThueMirrField(source_file, max_output=args.num)

    if DEBUG:
        [print(line) for line in f.unit_field]
        print("UNIT FIELD: %d x %d\n" % (f.unit_w, f.unit_h))

    while f.active():
        c = f.get_command()
        if DEBUG and c != ' ':
            k = f.current_key()                       # key, with current abs coords
            print("G:%d, %d " % (f.gx, f.gy), end='') # global coords of tile
            print("L:%d, %d " % (f.x, f.y), end='')   # local coords in current tile
            print("[%s] '%s' %s" % (k, c, f.hits.get(k, ''))) # num hits _including_ this one
            #print("   LAST OUTPUT:", f.last_output)
        f.advance()