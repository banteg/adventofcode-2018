from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import product, chain, count
from operator import attrgetter

import numpy as np
from PIL import Image

import aoc

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
    def above(self):
        return self + Point(0, -1)

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
        # only check for vertical bounds
        return point.y >= self.t and point.y <= self.b

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
        self.dirty = deque()
        self.clay = {p for p in self if self[p] == 'clay'}
        self.clay_on_row = defaultdict(set)
        for p in self.clay:
            self.clay_on_row[p.y].add(p)

    def stable(self, point):
        return self.get(point) in stable_states

    @property
    def still(self):
        return {p for p in self if self[p] == 'still'}

    @property
    def flowing(self):
        return {p for p in self if self[p] == 'flowing'}


def render_cli(grid, bounds, extra=None):
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
    while grid.dirty:
        water = grid.dirty.popleft()
        if grid.get(water) == 'flowing':
            fill_below(water, grid, bounds)
            still_water(water, grid)
            fill_sides(water, grid)


def fill_below(water, grid, bounds):
    fill = water.below
    while fill.y <= bounds.b and not grid.stable(fill):
        grid[fill] = 'flowing'
        fill = fill.below
    if fill != water.below:
        grid.dirty.append(fill.above)


def still_water(water, grid):
    if grid.stable(water.below):
        try:
            fill = Bounds(
                t=water.y,
                b=water.y,
                l=max(p.x + 1 for p in grid.clay_on_row[water.y] if p.x < water.x),
                r=min(p.x - 1 for p in grid.clay_on_row[water.y] if p.x > water.x),
            )
        except ValueError:  # no clay at this level
            pass
        else:
            below = Bounds(
                t=water.below.y,
                b=water.below.y,
                l=fill.l,
                r=fill.r
            )
            if all(grid.stable(p) for p in below):
                for p in fill:
                    grid[p] = 'still'
                    grid.dirty.append(p.above)


def fill_sides(water, grid):
    fill = water
    while grid.stable(fill.below) and not grid.stable(fill.left):
        grid[fill.left] = 'flowing'
        fill = fill.left
    if fill != water:
        grid.dirty.append(fill)

    fill = water
    while grid.stable(fill.below) and not grid.stable(fill.right):
        grid[fill.right] = 'flowing'
        fill = fill.right
    if fill != water:
        grid.dirty.append(fill)


def simulate(data):
    clay = [Clay.from_string(x) for x in data.splitlines()]
    grid = Grid({p: 'clay' for p in chain.from_iterable(clay)})
    bounds = Bounds.from_points(grid)
    tap = Point(500, 0)
    grid[tap.below] = 'flowing'
    grid.dirty.append(tap.below)
    spread_water(grid, bounds)
    return len([x for x in grid.still if x in bounds]), len([x for x in grid.flowing if x in bounds])


example = '''\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504'''


@aoc.test({example: 57})
def part_1(data: aoc.Data):
    still, flowing = simulate(data)
    return still + flowing


@aoc.test({example: 29})
def part_2(data: aoc.Data):
    still, flowing = simulate(data)
    return still
