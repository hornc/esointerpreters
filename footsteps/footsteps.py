#!/usr/bin/env python3
import re
import sys


"""
Minimal Python3 interpreter for Footsteps.
https://esolangs.org/wiki/Footsteps
"""


REF = re.compile(r'\s*(start|end)\s*')
SEP = '\n👣\n'


def loadfile(filename):
    with open(filename, 'r') as f:
        return [[int(REF.sub(lambda m: '-' * ('end' in m[0]), v)) for v in line.strip().split(',') if v] for line in f]


def run(rows):
    try:
        while rows := rows[1:] + [rows[c] for c in rows[0]]: print(rows, end=SEP)
    except IndexError:
        pass


if __name__ == '__main__':
    run(loadfile(sys.argv[1]))
