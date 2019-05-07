from dataclasses import dataclass
from operator import attrgetter

import aoc


@dataclass(frozen=True)
class Nanobot:
    x: int
    y: int
    z: int
    r: int

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


example = '''
    pos=<0,0,0>, r=4
    pos=<1,0,0>, r=1
    pos=<4,0,0>, r=3
    pos=<0,2,0>, r=1
    pos=<0,5,0>, r=3
    pos=<0,0,3>, r=1
    pos=<1,1,1>, r=1
    pos=<1,1,2>, r=1
    pos=<1,3,1>, r=1
    '''


@aoc.test({example: 7})
def part_1(data: aoc.Data):
    bots = [Nanobot(*x) for x in data.ints_lines]
    strongest = max(bots, key=attrgetter('r'))
    return sum(1 for x in bots if strongest.distance(x) <= strongest.r)
