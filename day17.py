from collections import defaultdict
from dataclasses import dataclass
from itertools import product, chain, count
from operator import attrgetter
from time import time

import numpy as np
from PIL import Image

import aoc

reading_order = attrgetter('y', 'x')
stable_states = {'clay', 'still'}
frame = count()
scale = 1


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
        # only check vertical bounds
        return all([
            # point.x >= self.l, point.x <= self.r,
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

    def __init__(self, data):
        super().__init__(data)
        self.cache = defaultdict(set)
        for p in self:
            self.cache[self[p]].add(p)
        self.clay = {p for p in self if self[p] == 'clay'}
        self.clay_on_row = defaultdict(set)
        for p in self.clay:
            self.clay_on_row[p.y].add(p)

    def __setitem__(self, key, value):
        last = self.get(key)
        self.cache[last].discard(key)
        self.cache[value].add(key)
        dict.__setitem__(self, key, value)

    @property
    def still(self):
        return set(self.cache['still'])

    @property
    def flowing(self):
        return set(self.cache['flowing'])


def render(grid, bounds, extra=None):
    if extra is None:
        extra = []
    msg = ''
    symbols = {
        'clay': '#',
        'tap': '+',
        'flowing': '|',
        'still': '~',
        None: '.',
    }
    for row in bounds.to_points():
        for p in row:
            if p in extra:
                msg += '*'
            else:
                msg += symbols.get(grid.get(p, None))
        msg += '\n'
    print(msg)


def render_image(grid, bounds):
    colors = {
        'clay': [59, 66, 82],
        'tap': [180, 142, 173],
        'flowing': [129, 161, 193],
        'still': [94, 129, 172],
        None: [236, 239, 244],
    }
    data = []
    for row in bounds.to_points():
        data.append([])
        for p in row:
            data[-1].append(colors.get(grid.get(p, None)))
    arr = np.array(data)
    img = Image.fromarray(arr.astype(np.uint8))
    w, h = img.size
    img = img.resize((w * scale, h * scale))
    img.save(f'renders/{next(frame):04d}.png')


def spread_water(grid, bounds):
    flow_down(grid, bounds)
    still_water(grid, bounds)
    flow_sides(grid, bounds)


def flow_down(grid, bounds):
    for water in grid.flowing:
        fill = water.below
        # edge case: tap can be higher than the first clay, so we only check the bottom bound
        while fill.y <= bounds.b and grid.get(fill) not in stable_states:
            grid[fill] = 'flowing'
            fill = fill.below


def still_water(grid, bounds):
    for water in grid.flowing:
        if grid.get(water.below) in stable_states:
            try:
                fill = Bounds(
                    t=water.y,
                    b=water.y,
                    l=max(p.x + 1 for p in grid.clay_on_row[water.y] if p.x < water.x),
                    r=min(p.x - 1 for p in grid.clay_on_row[water.y] if p.x > water.x),
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


def flow_sides(grid, bounds):
    for water in grid.flowing:
        # fill left
        fill = water
        while grid.get(fill.below) in stable_states and grid.get(fill.left) not in stable_states:
            grid[fill.left] = 'flowing'
            fill = fill.left
        # fill right
        fill = water
        while grid.get(fill.below) in stable_states and grid.get(fill.right) not in stable_states:
            grid[fill.right] = 'flowing'
            fill = fill.right


def simulate(data, vis=False):
    clay = [Clay.from_string(x) for x in data.splitlines()]
    grid = Grid({p: 'clay' for p in chain.from_iterable(clay)})
    bounds = Bounds.from_points(grid)
    render_bounds = Bounds.from_points(grid)
    tap = Point(500, 0)
    grid[tap] = 'tap'
    grid[tap.below] = 'flowing'

    last = None
    while grid != last:
        last = grid.copy()
        start = time()
        spread_water(grid, bounds)
        a, b = len(grid.cache['still']), len(grid.cache['flowing'])
        print(f'total={a+b} still={a} flowing={b} time={(time() - start) * 1000:.3f}ms')
    print('part 2', len([x for x in grid.still if x in bounds]))
    return len([x for x in grid.still | grid.flowing if x in bounds])


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
    return simulate(data, vis=False)
