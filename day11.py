import numpy as np

import aoc

examples = {
    (122, 79, 57): -5,
    (217, 196, 39): 0,
    (101, 153, 71): 4,
}


def cell_power(x, y, serial):
    rack = x + 10
    return ((rack * y + serial) * rack) % 1000 // 100 - 5


def load_grid(serial):
    return np.fromfunction(lambda x, y: cell_power(x, y, serial), (301, 301))


@aoc.test({})
def part_1(data: aoc.Data):
    for case, expected in examples.items():
        assert cell_power(*case) == expected

    serial = int(data)
    grid = load_grid(serial)

    best, bx, by = float('-inf'), 0, 0
    for y in range(1, 299):
        for x in range(1, 299):
            power = np.sum(grid[y:y + 3, x:x + 3])
            if power > best:
                best, bx, by = power, x, y
    return f'{bx},{by}'


@aoc.test({})
def part_2(data: aoc.Data):
    serial = int(data)
    grid = load_grid(serial)

    best, bx, by, bs = float('-inf'), 0, 0, 0
    for s in range(1, 301):
        for y in range(1, 301 - s):
            for x in range(1, 301 - s):
                power = np.sum(grid[y:y + s, x:x + s])
                if power > best:
                    best, bx, by, bs = power, x, y, s
        if s >= bs + 5:
            # exit early if no improvement
            break
    return f'{bx},{by},{bs}'
