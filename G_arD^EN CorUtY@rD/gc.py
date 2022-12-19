#!/usr/bin/env python

"""
Esoteric programming language interpreter for
G_arD^EN CorUtY@rD
https://esolangs.org/wiki/G_arD%5EEN_CorUtY@rD
Interpreter by Salpynx, 2022.
"""

import sys
import re
from time import sleep

NAME = 'G_arD^EN CorUtY@rD'
ARROWS = '>v<^'
PAUSE = 0.1  # pause time between frames in seconds
DEBUG = False 
LIMIT = 3000
PRE = '\033['
RST = PRE + '0m'
CLR = '\033c'
WHITE = '1;37m'
BROWN = '0;33m'
SOIL = BROWN
FENCE = WHITE
LCYAN = '1;36m'
RED = '1;31m'
GREEN = '0;32m'
LG = '1;32m'
BLUE = '0;34m'
PATH = '1;33m'
LGREY = '1;37m'
GREY = '1;30m'
MAGENTA = '1;35m'

COLORS = {
        'x': FENCE,
        'X': FENCE,
        'K': FENCE,
        'L': LCYAN,
        '#': RED,
        '~': GREEN,
        '=': SOIL,
        '+': BLUE,
        '-': PATH,
        ':': GREY,
        'E': GREY,
        'T': WHITE,
        '_': RED,
        '>': LG,
        '<': LG,
        '^': LG,
        'v': LG,
        '@': MAGENTA,
        }


def color(s):
    """Return an ANSI colored string based on first symbol."""
    c = COLORS.get(s[0], '0m')
    return PRE + c + s + RST


class GardenCourtyard:
    def __init__(self, source):
        self.source = source
        self.width = len(source[0])
        self.height = min([n for n,v in enumerate(source) if '_' in v])
        self.ip = self.findfirstchair()
        self.dir = 0  # 0: right (down, left, up)
        self.soil = self.source[0][:self.source[0].find('K')].replace('x', '0').replace('X', '1')
        self.cq = ''  # Command queue
        self.oq = ''  # Output queue
        self.output = ''

    def findfirstchair(self):
        for y, line in enumerate(self.source):
            for x, c in enumerate(line):
                if c == 'L':
                    return [x, y]

    def show(self):
        print(CLR + PRE + MAGENTA + NAME + RST) 
        for j, line in enumerate(self.source):
            if j == 0:  # soil / datastring / fence
                if len(self.soil) < self.width:
                    line = self.soil + 'K' + line[len(self.soil) + 1:]
                else:
                    line = self.soil
                line = line.replace('0', 'x').replace('1', 'X')
            if j == self.ip[1]:
                x = self.ip[0]
                c = line[x]
                line = line[:x] + '@' + line[x+1:]
            runs = re.findall(r'((.)\2*)', line)
            for run in runs:
                block, symbol = run
                print(color(block), end='')
            print()

    def process(self, c):
        if c == '~':
            self.cq += '0'
            self.dir = 1
        elif c == '+':
            self.cq += '1'
            self.dir = 0
        elif c == '-':
            if self.soil[-1] == '0':
                self.dir = 0
            else:
                self.dir = 1
        elif c == ':':
            self.cq += c
            self.dir = 1
        elif c == '=':
            cc = self.cq[0]
            self.cq = self.cq[1:]
            if cc == ':':
                self.soil = self.soil[1:]
            else:
                if self.soil[0] == '1':
                    self.soil = self.soil + cc
        elif c == 'E':
            self.oq += self.soil[0]
            self.soil = self.soil[1:]
            if len(self.oq) == 8:
                self.output += chr(int(self.oq, 2))
                self.oq = ''
                #self.dir = 0
        elif c in ARROWS: 
            self.dir = ARROWS.find(c)

        d = self.dir
        x, y = self.ip

        if d & 1:
            y += 1 - (d - 1) 
        else:
            x += 1 - d
        self.ip = [x, y]

    def run(self):
        running = True
        i = 0
        while running:
            x, y = self.ip
            if y == self.height:
                break
            self.show()
            c = self.source[y][x]
            self.process(c)
            if DEBUG:
                print('Current command:', c)
                print(self.ip, self.dir)
                print('DATA STRING:', self.soil)
                print(i)
                print('CQ:', self.cq)
                print('OQ:', self.oq)
            print(f'>:{self.output}')
            sleep(PAUSE)
            i += 1
            if i > LIMIT:
                break


if __name__ == '__main__':
    sourcefile = sys.argv[1]
    source = []
    width = 0
    with open(sourcefile, 'r') as f:
        for line in f.readlines():
            line = line.strip("\n")
            width = len(line)
            source.append(line)

    gc = GardenCourtyard(source)
    gc.run()