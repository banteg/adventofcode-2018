from dataclasses import dataclass
from typing import Union
from itertools import product, chain
from operator import attrgetter

from click import style

import aoc

reading_order = attrgetter('y', 'x')
stable_states = {'clay', 'still'}


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    @property
    def below(self):
        return self + Point(0, 1)
    
    @property
    def left(self):
        return self + Point(-1, 0)
    
    @property
    def right(self):
        return self + Point(1, 0)


@dataclass
class Bounds:
    t: int
    l: int
    b: int
    r: int

    @classmethod
    def from_points(cls, points: [Point]):
        return cls(
            t=min(p.y for p in points),
            l=min(p.x for p in points),
            r=max(p.x for p in points),
            b=max(p.y for p in points),
        )

    def __contains__(self, point: Point):
        return all([
            point.x >= self.l, point.x <= self.r,
            point.y >= self.t, point.y <= self.b,
        ])

    def __iter__(self):
        for x, y in product(range(self.l, self.r + 1), range(self.t, self.b + 1)):
            yield Point(x, y)
    
    def to_points(self):
        return [
            [Point(x, y) for x in range(self.l, self.r + 1)]
            for y in range(self.t, self.b + 1)
        ]


@dataclass
class Clay:
    x: range
    y: range

    @classmethod
    def from_string(cls, data):
        coords = dict(x.split('=') for x in data.split(', '))
        for k in coords:
            v = [int(x) for x in coords[k].split('..')]
            coords[k] = range(v[0], v[1] + 1) if len(v) == 2 else range(v[0], v[0] + 1)
        return cls(**coords)

    def __iter__(self):
        for x, y in product(self.x, self.y):
            yield Point(x, y)



class Grid(dict):
    
    @property
    def clay(self):
        return {p for p in self if self[p] == 'clay'}

    @property
    def still(self):
        return {p for p in self if self[p] == 'still'}

    @property
    def flowing(self):
        return {p for p in self if self[p] == 'flowing'}

    @property
    def occupied(self):
        return self.clay | self.still




def render(grid, bounds, extra=None):
    if extra is None:
        extra = []
    msg = ''
    symbols = {
        'clay': '#',
        'tap': '+',
        'flowing': style('|', fg='blue', bold=True),
        'still': style('~', fg='blue', bold=True),
        None: style('.', dim=True),
    }
    for row in bounds.to_points():
        for p in row:
            if p in extra:
                msg += style('*', fg='green', bold=True)
            else:
                msg += symbols.get(grid.get(p, None))
        msg += '\n'
    print(msg)


def spread_water(grid, bounds):
    # flow down
    for water in grid.flowing:
        fill = water.below
        while fill in bounds and fill not in grid.occupied:
            grid[fill] = 'flowing'
            fill = fill.below

    # stabilize still water
    for water in grid.flowing:
        if water.below in grid.occupied:
            try:
                fill = Bounds(
                    t=water.y,
                    b=water.y,
                    l=max(p.x + 1 for p in grid.clay if p.y == water.y and p.x < water.x),
                    r=min(p.x - 1 for p in grid.clay if p.y == water.y and p.x > water.x),
                )
            except ValueError:  # no clay at this level
                continue
            below = Bounds(
                t=water.below.y,
                b=water.below.y,
                l=fill.l,
                r=fill.r,
            )
            stabilized = {grid.get(p) for p in below} <= stable_states
            if stabilized:
                for p in fill:
                    grid[p] = 'still'

    # flow to the sides
    for water in grid.flowing:
        stable = grid.get(water.below) in stable_states
        if stable and water.left not in grid.occupied:
            grid[water.left] = 'flowing'
        if stable and water.right not in grid.occupied:
            grid[water.right] = 'flowing'


def simulate(data, vis=False):
    gravity = Point(0, 1)
    clay = [Clay.from_string(x) for x in data.splitlines()]
    grid = Grid({p: 'clay' for p in chain.from_iterable(clay)})
    bounds = Bounds.from_points(grid)
    tap = Point(500, 0)
    grid[tap] = 'tap'
    grid[tap.below] = 'flowing'

    # produce water
    last = None
    for i in range(10):
    # while grid != last:
        last = grid.copy()
        spread_water(grid, bounds)
        if vis:
            render(grid, bounds)
        else:
            print(i, len(grid.still | grid.flowing))
    return len(grid.still | grid.flowing)


examples = {'''\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504''': 57}


@aoc.test(examples)
def part_1(data: aoc.Data):
    return simulate(data, vis=data in examples)
