#!/usr/bin/env python3
import argparse
from mpmath import mp, mpf, sqrt


ABOUT = """
Interpreter for esolang Conedy
https://esolangs.org/wiki/Conedy

Language by ais523, 2017.
This interpreter by Salpynx, 2024.
"""

ENDIANNESS = 0  # 0 = little, 1 = big

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
        self.byte_buffer = []
        self.output_buffer = ''
        xmax = ymax = 0
        assert self.source[0][0].islower(), f'Expected top-left to be a net (lowercase). Got: {self.source[0][0]}'
        for y, line in enumerate(self.source):
            for x, c in enumerate(line):
                if not c.strip():
                    continue
                if c.isupper():
                    if c in self.beacons:
                        assert not isinstance(self.beacons[c], tuple), f'ERROR: More than two Beacons: {c}!'
                        self.beacons[c] = (self.beacons[c], Beacon(c, x, y))
                    else:
                        self.beacons[c] = Beacon(c, x, y)
                else:
                    if c in self.nets:
                        assert not isinstance(self.nets[c], tuple), f'ERROR: More than two Nets: {c}!'
                        self.nets[c] = (self.nets[c], Net(c, x, y))
                    else:
                        self.nets[c] = Net(c, x, y)
                if x > xmax:
                    xmax = x
                if y > ymax:
                    ymax = y
        self.bounds = [xmax, ymax]
        # Associate all nets with the correct Beacon
        for beacon in self.beacons:
            n = beacon.casefold()
            if isinstance(self.nets[n], tuple):
                self.nets[n][0].beacon = self.nets[n][1].beacon = beacon
            else:
                self.nets[n].beacon = beacon
        print('Beacons:', self.beacons)
        print('Nets:', self.nets)
        print('Bounds:', self.bounds)
        print()

    def run(self):
        self.set_target(self.source[0][0])
        print(f'Initial state = {self.ip}')
        while self.ip.target:
            self.ticks += 1
            self.next_collision()
            print(f'  {self.ip}')
            if self.ip.target is None:
                print(f'IP has left the playfield at {self.ip}!')
        if self.output_buffer:
            print(self.output_buffer)

    def checkpos(self, x, y) -> str:
        try:
            return self.source[y][x].strip()
        except IndexError:
            return ''

    def set_target(self, net:str, pos=(0, 0)):
        net = net.casefold()
        x, y = pos
        if isinstance(self.nets[net], tuple):  # OUTPUT 1 bit!
            a, b = self.nets[net]
            bit = 0 if a.y == y and a.x == x else 1
            self.output(bit)
            beacon = self.beacons[a.beacon]
        else:
            beacon = self.beacons[self.nets[net].beacon]
        if isinstance(beacon, tuple):
            print('TODO: Get 1 bit of input to choose target!')
            beacon = beacon[0]
        self.ip.target = beacon

    def output(self, bit):
        self.byte_buffer.append(bit)
        b = ''.join([str(i) for i in self.byte_buffer])[::ENDIANNESS * 2 - 1]
        if len(b) == 8:
            c = chr(int(b, 2))
            print('OUTPUT:', c)
            self.output_buffer += c
            self.byte_buffer = []

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
            print(f'  Initial lengths: {lenx}, {leny}')
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
                self.set_target(c, pos)
            if pos[0] < 0 or pos[1] < 0 or pos[0] > self.bounds[0] or pos[1] > self.bounds[1]:
                # out of bounds!
                collided = True
                self.ip.target = None
        # for one.con example:
        # slope: (5.5 - 0.5) / (16.5 - 0.5) = 0.3125
        # exit point: x = 17
        # y = 17 * 0.3125 + 0.5 = 5.8125 
        # x = 17.0
        target = self.ip.target
        collision = 'boundary' if target is None else f'net {target.id.casefold()}'
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
