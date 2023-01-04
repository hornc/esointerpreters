#!/usr/bin/env python3
import sys

"""
Interpreter for esolang Barely
https://esolangs.org/wiki/Barely

2023. Salpynx.
"""


class Barely:
    def __init__(self, source):
        self.source, self.input = source.strip().split('~')
        self.tape = {}
        self.mp = 0
        self.ip = len(self.source) - 1
        self.jmp = 0
        self.acc = 126

    def run(self):
        while self.ip > 0:
            c = self.source[self.ip]
            self.ip -= 1
            self.exec(c)


    def exec(self, c):
        match c:
            case ']':
                self.ip = -1
            case '^' | 'b':
                if c == 'b' or self.acc == 0:
                   self.ip += self.jmp
            case 'g':
                self.acc = self.tape.get(self.mp, 0)
                self.exec('i')
            case 'h':
                self.acc += 71
                self.exec('k')
            case 'i':
                self.mp += 1
                self.exec('j')
            case 'j':
                self.acc += 1
                self.exec('k')
            case 'k':
                self.jmp -= 1
            case 'm':
                self.tape[mp] = self.acc
                self.exec('o')
            case 'n':
                self.mp -= 1
                self.exec('o')
            case 'o':
                self.acc -= 1
                self.exec('p')
            case 'p':
                self.jmp += 10
            case 't':
                self.acc = ord(self.input[0])
                self.input = self.input[1:]
            case 'x':
                print(chr(self.acc), end='')
        self.acc = self.acc % 256


def main(source):
    b = Barely(source)
    b.run()


if __name__ == '__main__':
    source = sys.stdin.read()
    main(source)
