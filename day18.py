from collections import Counter
from dataclasses import dataclass
from itertools import product, count

import numpy as np

import aoc

open_ground, trees, lumberyard = '.|#'
near8 = {(x, y) for x, y in product((-1, 0, 1), (-1, 0, 1))} - {(0, 0)}


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

    def run(self):
        for t in range(10):
            self.advance_time()
        return self.resource_value

    def run_forever(self, goal: int):
        seen = []
        start = None
        for t in count(1):
            self.advance_time()
            r = self.resource_value
            if r not in seen:
                start = None
            elif start is None:
                start = t + 1
            if start and t > start + 3 and r == seen[start]:
                size = t - start
                return seen[start + (goal - 1 - start) % (size - 1)]
            print(t, end='\r')
            seen.append(r)

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
    '''
    .#.#...|#.
    .....#|##|
    .|..|...#.
    ..|#.....#
    #.#|||#|#|
    ...#.||...
    .|....|...
    ||...#|.#|
    |.||||..|.
    ...#.|..|.
    ''': 1147
}


@aoc.test(examples)
def part_1(data: aoc.Data):
    grid = Grid.from_string(data)
    return grid.run()


@aoc.test({})
def part_2(data: aoc.Data):
    grid = Grid.from_string(data)
    return grid.run_forever(1_000_000_000)
