from collections import Counter
from dataclasses import dataclass
from itertools import product, zip_longest
from operator import attrgetter

import numpy as np
import pyglet
from pyglet.gl import *
from PIL import Image

import aoc


open_ground = '.'
trees = '|'
lumberyard = '#'

window = pyglet.window.Window(500, 500, caption='aoc 2018 day 18')


@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    @property
    def near(self):
        deltas = {Point(x, y) for x, y in product((-1, 0, 1), (-1, 0, 1))} - {Point()}
        return [self + delta for delta in deltas]


@dataclass
class Grid:
    grid: {Point: str}

    @classmethod
    def from_string(cls, data):
        grid = {}
        for y, row in enumerate(data.splitlines()):
            for x, s in enumerate(row):
                grid[Point(x, y)] = s
        return cls(grid)

    def __repr__(self):
        msg = ''
        ordered = sorted(self.grid, key=attrgetter('y', 'x'))
        for a, b in zip_longest(ordered, ordered[1:], fillvalue=Point(0, 0)):
            msg += self.grid[a]
            if a.y != b.y:
                msg += '\n'
        return msg

    def render(self):
        colors = {
            '.': [215, 222, 233],
            '|': [163, 190, 140],
            '#': [209, 135, 112],
        }
        data = []
        for y in range(50):
            data.append([])
            for x in range(50):
                data[-1].append(colors[self.grid[Point(x, y)]])
        arr = np.array(data)
        img = Image.fromarray(arr.astype(np.uint8))
        img.save('1.png')
        w, h, d = arr.shape
        im = pyglet.image.ImageData(w, h, 'RGB', img.tobytes())
        window.dispatch_events()
        window.switch_to()
        window.clear()
        scale = min(window.width / im.texture.width, window.height / im.texture.height)
        im.texture.width *= scale
        im.texture.height *= scale
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        im.blit(0, 0)
        window.flip()

    def run(self):
        for t in range(10):
            self.advance_time()
        return self.resource_value

    def advance_time(self):
        temp = self.grid.copy()
        for p in temp:
            near = Grid.near(temp, p)
            self.grid[p] = Grid.transform(temp[p], near)

    @staticmethod
    def near(grid, point):
        near = [grid.get(p) for p in point.near]
        return [x for x in near if x is not None]

    @staticmethod
    def transform(s, near):
        c = Counter(near)
        if s == open_ground:
            return trees if c[trees] >= 3 else s
        if s == trees:
            return lumberyard if c[lumberyard] >= 3 else s
        if s == lumberyard:
            return lumberyard if c[lumberyard] >= 1 and c[trees] >= 1 else open_ground
        return s

    @property
    def resource_value(self):
        c = Counter(self.grid.values())
        return c[trees] * c[lumberyard]


examples = {
'''\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.''': 1147
}


@aoc.test(examples)
def part_1(data: aoc.Data):
    grid = Grid.from_string(data)
    return grid.run()

