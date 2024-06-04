#!/usr/bin/env python3
import argparse
from random import shuffle
from time import sleep


ABOUT = """Doors esolang interpreter
  https://esolangs.org/wiki/Doors

  Language spec by BestCoder, 2024.
  This interpreter by Salpynx, 2024.
"""

EYES = ".:👀\u0307\u0325\u0323\u030A:."  # meh?
DOOR = "🚪"


class Player:
    def __init__(self):
        self.value = 0
        self.direction = 1  # 1: fwd, -1: rev


def run(doors, p):
    running = True
    ptr = 1  # ptr is 1 based index
    while running:
        c, v = doors[ptr - 1]
        ptr += p.direction
        #print('ENTITY:', c)
        if c == 'v':  # void, teleport to door v
            ptr = v
            #print(f'Jump to {DOOR} {ptr}')
        elif c == 'e':  # eyes, input
            eyes = list(EYES)
            shuffle(eyes)  # TODO: this isn't as succesful as I hoped...
            in_ = input(''.join(eyes) + ' ')
            if in_:
                p.value = ord(in_[0])
            else:
                p.value = 0x0A  # newline
        elif c == 't':
            #print(chr(p.value))
            print(p.value)
        elif c == 'r':  # rush
            p.value += 1
        elif c == 'a':
            p.value += v
        elif c == 's':  # Screech, reverse
            p.dir = p.direction * -1
        elif c == 'S':  # seek!
            sleep(v)
        elif c == 'f':  # figure, cond eq
            if p.value != v:  # continue if equal, else jump to door v
                ptr = v
        elif c == 'g':  # guiding light
            p.value -= 1
        elif c == 'c':  # curious light
            p.value -= v
        elif c == 'd':  # dupe , reverse of figure
            if p.value == v:
                ptr = v
        elif c == 'j':  # jack ... (jump?)
            ptr = p.value
        elif c == 'G':
            p.value = v
            #print(f'Player value = {p.value}')

        if ptr < 1 or ptr > len(doors) or c == 'h':
            running = False 


def main():
    parser = argparse.ArgumentParser(description=ABOUT, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('source', help='Source file to process', type=argparse.FileType('r'))
    parser.add_argument('--debug', '-d', help='Turn on debug output', action='store_true')
    args = parser.parse_args()

    source = args.source.read()
    print('SOURCE:')
    print(source)

    doors = []  # list of numbered doors
    entities, values = source.split('\n')[:2]
    #print(entities, values)

    i = 0
    for entity in entities:
        if entity.strip():
            doors.append((entity, int(values[i]) if values[i].strip() else None))
        elif values[i].strip():
            prev = doors[i-1]
            doors[i-1] = (prev[0], prev[1] * 10 + int(values[i]))
        i += 1

    print('ROOMS:' + ''.join([f'{DOOR}{i+1}{d}' for i,d in enumerate(doors)]) + '\n')

    player = Player()
    run(doors, player)


if __name__ == '__main__':
    main()
