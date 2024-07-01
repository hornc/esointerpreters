#!/usr/bin/env python3
import argparse
from mpmath import mp, mpf, sqrt


ABOUT = """
Interpreter for esolang Conedy
https://esolangs.org/wiki/Conedy

Language by ais523, 2017.
This interpreter by Salpynx, 2024.
"""

"""
Testing the question: Can a Conedy program
enter an infinite loop which has it passing through
the same patch of code space with a different data
value each time?
(If it can't, it is not TC)
ANS: Yes, it can, the basic loop.con example demonstrates this.
The ip should get ever closer to y=4.5 without ever reaching it.

TODO:
    * Confirm the basic algorithm is correct...
    * Clearly indicate when overflow has occurred
"""


class Beacon:
    def __init__(self, id_:str, x:int, y:int):
        self.id = id_
        self.x = x + 0.5
        self.y = y + 0.5

    def __repr__(self):
        return f'{self.id} @ {self.x}, {self.y}'


class Net:
    def __init__(self, id_:str, x:int, y:int):
        self.id = id_
        self.x = x
        self.y = y
        self.beacon = None

    def __repr__(self):
        return f'{self.id} @ {self.x}, {self.y} ⤞ {self.beacon}'


class Ip:
    def __init__(self):
        self.x = mpf(0.5)
        self.y = mpf(0.5)
        self.target = None

    def __repr__(self):
        return f'ip: ({self.x}, {self.y}) ⤞ {self.target}'


class Field:
    def __init__(self, source, debug=False):
        self.source = source.readlines()
        self.beacons = {}
        self.nets = {}
        self.ip = Ip()
        self.ticks = 0
        self.debug = debug
        xmax = ymax = 0
        assert self.source[0][0].islower(), f'Expected top-left to be a net (lowercase). Got: {self.source[0][0]}'
        for y, line in enumerate(self.source):
            for x, c in enumerate(line):
                if not c.strip():
                    continue
                if c.isupper():
                    self.beacons[c] = Beacon(c, x, y)
                else:
                    self.nets[c] = Net(c, x, y)
                if x > xmax:
                    xmax = x
                if y > ymax:
                    ymax = y
        self.bounds = [xmax, ymax]
        # Associate all nets with the correct Beacon
        for beacon in self.beacons:
            self.nets[beacon.casefold()].beacon = beacon
        print('Beacons:', self.beacons)
        print('Nets:', self.nets)
        print('Bounds:', self.bounds)
        print()

    def run(self):
        beacon = self.source[0][0].upper()
        self.ip.target = self.beacons[beacon]
        print(f'Initial state = {self.ip}')
        while self.ip.target:
            self.ticks += 1
            self.next_collision()
            print(f'  {self.ip}')
            if self.ip.target is None:
                print(f'IP has left the playfield at {self.ip}!')

    def checkpos(self, x, y) -> str:
        try:
            return self.source[y][x].strip()
        except IndexError:
            return ''

    def next_collision(self):
        """
        Sets the next ip position, and next target beacon,
        or set ip.target to None for out of bounds.

        Uses Digital Differential Analysis (DDA) ray-casting algorithm
          via https://www.youtube.com/watch?v=NbSee-XM7WA
          and https://lodev.org/cgtutor/raycasting.html
        """
        x = self.ip.x
        y = self.ip.y
        tx = self.ip.target.x
        ty = self.ip.target.y
        slope = mpf('inf') if tx == x else (ty - y)/(tx - x)
        assert isinstance(slope, mpf), f'slope is {type(slope)}, expecting mpf'
        ustepx = sqrt(1 + slope**2)
        ustepy = mpf('inf') if slope == 0 else sqrt(1 + (1/slope)**2)
        assert isinstance(ustepy, mpf)
        if self.debug:
            print('  SLOPE:', slope)
            print('  Unit Steps:', ustepx, ustepy)
        pos = [int(x), int(y)]  # current checking pos
        lenx = leny = 0
        if tx < x:
            stepx = -1
            lenx = (x - pos[0]) * ustepx
        else:
            stepx = 1
            lenx = (pos[0] + 1 - x) * ustepx
        if ty < y:
            stepy = -1
            leny = (y - pos[1]) * ustepy
        else:
            stepy = 1
            leny = (pos[1] + 1 - y) * ustepy
        if self.debug:
            print(f'  Initial lengths: {lenx}, {leny}')  # why can these be so large?
               # Makes sense that the y unit step should be giant on a very shallow slope
               # the alg. picks the _shortest_ length to travel, makes sense that the ignored one could be very large..
        collided = False
        while not collided:
            if lenx < leny:
                step = 'X'
                pos[0] += stepx
                lenx += ustepx
            else:
                step = 'Y'
                pos[1] += stepy
                leny += ustepy
            c = self.checkpos(*pos)
            if self.debug:
                print('Cell:', pos, c)
            if c and c.islower():
                collided = True
                self.ip.target = self.beacons[self.nets[c].beacon]
            if pos[0] < 0 or pos[1] < 0 or pos[0] > self.bounds[0] or pos[1] > self.bounds[1]:
                # out of bounds!
                collided = True
                self.ip.target = None
        # for one.con example:
        # slope: (5.5 - 0.5) / (16.5 - 0.5) = 0.3125
        # exit point: x = 17
        # y = 17 * 0.3125 + 0.5 = 5.8125 
        # x = 17.0
        collision = 'boundary' if self.ip.target is None else f'net {self.ip.target.id.casefold()}'
        print(f'Event {self.ticks}:')
        if step == 'X':
             # collision on x step
             self.ip.x = pos[0]
             print(f'  X collision: {pos}, at {collision}')
             self.ip.y = pos[0] * slope + y
        else:  # collision on y step
             self.ip.y = pos[1]
             print(f'  Y collision: {pos}, at {collision}')
             self.ip.x = mpf(pos[0]) if slope == 0 else pos[1] * (1/slope) + x


def main():
    parser = argparse.ArgumentParser(description=ABOUT, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('source', help='Source file to process', type=argparse.FileType('r'))
    parser.add_argument('--precision', '-p', help='Precision (decimal places)', default=200, type=int)
    parser.add_argument('--debug', '-d', help='Turn on debug output', action='store_true')
    args = parser.parse_args()

    mp.dps = args.precision
    print(f'Conedy interpreter. Loading {args.source.name}\n')
    field = Field(args.source, debug=args.debug)

    field.run()


if __name__ == '__main__':
    main()
