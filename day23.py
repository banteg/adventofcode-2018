from dataclasses import dataclass
from operator import attrgetter
from collections import Counter, defaultdict
from itertools import combinations

from z3 import Ints, Int, If, Optimize, Sum
import networkx as nx

import aoc


@dataclass(frozen=True)
class Nanobot:
    x: int
    y: int
    z: int
    r: int = 0

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


example_2 = '''
    pos=<10,12,12>, r=2
    pos=<12,14,12>, r=2
    pos=<16,12,12>, r=4
    pos=<14,14,14>, r=6
    pos=<50,50,50>, r=200
    pos=<10,10,10>, r=5
    '''


def solve_z3(bots):
    
    def Abs(x):
        return If(x >= 0, x, -x)
    
    def Dist(a, b):
        return Abs(a[0] - b[0]) + Abs(a[1] - b[1]) + Abs(a[2] - b[2])

    def dist(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

    start = 0, 0, 0
    x, y, z = Ints('x y z')
    pos = x, y, z
    near = Int('near')
    
    dist_from_start = Dist(start, pos)
    nanobots_in_range = Sum([If(Dist(bot, pos) <= r, 1, 0) for *bot, r in bots])
    
    opt = Optimize()
    opt.add(near == nanobots_in_range)
    opt.maximize(near)
    opt.minimize(dist_from_start)

    opt.check()
    model = opt.model()
    final = [model[i].as_long() for i in pos]
    return dist(start, final)


def solve_nx(bots):

    def manhattan_distance(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)

    def overlap(bots):
        return manhattan_distance(*bots) <= bots[0].r + bots[1].r

    def signed_distance_function(bot):
        return abs(bot.x) + abs(bot.y) + abs(bot.z) - bot.r

    G = nx.Graph()
    bots = [Nanobot(*bot) for bot in bots]
    G.add_edges_from(filter(overlap, combinations(bots, 2)))
    clique = max(nx.find_cliques(G), key=len)
    return max(map(signed_distance_function, clique))


@aoc.test({example_2: 36})
def part_2(data: aoc.Data):
    # return solve_z3(data.ints_lines)
    return solve_nx(data.ints_lines)
