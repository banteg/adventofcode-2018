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

near8 = {(x, y) for x, y in product((-1, 0, 1), (-1, 0, 1))} - {(0, 0)}

window = pyglet.window.Window(500, 500, caption='aoc 2018 day 18')


@dataclass
class Grid:
    grid: np.array

    @classmethod
    def from_string(cls, data):
        rows = [list(row) for row in data.splitlines()]
        grid = np.array(rows)
        return cls(grid)

    def __repr__(self):
        return '\n'.join(''.join(row) for row in self.grid)

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
        before = self.grid.copy()
        for y, row in enumerate(self.grid):
            for x, s in enumerate(row):
                near = Grid.near(before, x, y)
                self.grid[y, x] = Grid.transform(before[y, x], near)

    @staticmethod
    def near(grid, x, y):
        return [
            grid[y + dy, x + dx] for dx, dy in near8
            if 0 <= y + dy < grid.shape[0] and 0 <= x + dx < grid.shape[1]
        ]

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
        c = Counter(self.grid.flatten())
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

