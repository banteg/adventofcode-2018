import aoc
from itertools import chain
from collections import Counter
import numpy as np


example = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''


def bounds(coordinates):
    t = min(coordinates, key=lambda c: c[1])[1]
    l = min(coordinates, key=lambda c: c[0])[0]
    b = max(coordinates, key=lambda c: c[1])[1]
    r = max(coordinates, key=lambda c: c[0])[0]
    return t, l, b, r


def closest(x, y, coordinates):
    distances = Counter({
        c: abs(x - dx) + abs(y - dy)
        for c, (dx, dy) in enumerate(coordinates, 1)
    })
    n = min(distances, key=lambda x: distances[x])
    # equally distant locations are ignored
    if len([x for x in distances if distances[x] == distances[n]]) > 1:
        return 0
    return n


def vicinity(x, y, coordinates):
    distances = Counter({
        c: abs(x - dx) + abs(y - dy)
        for c, (dx, dy) in enumerate(coordinates, 1)
    })
    return sum(distances.values())


@aoc.test({example: 17})
def part_1(data: aoc.Data):
    coordinates = data.ints_lines
    t, l, b, r = bounds(coordinates)
    area = np.zeros((b - t + 1, r - l + 1))
    for y in range(t, b + 1):
        for x in range(l, r + 1):
            c = closest(x, y, coordinates)
            area[y - t][x - l] = c
    # areas around borders are infinite
    infinite = set(area[0][:]) | set(area[-1][:]) | set(area[:][0]) | set(area[:][-1])
    areas = Counter(chain.from_iterable(area)).most_common()
    areas = [size for n, size in areas if n not in infinite]
    return areas[0]


@aoc.test({example: 16})
def part_2(data: aoc.Data):
    coordinates = data.ints_lines
    max_vicinity = 32 if len(coordinates) == 6 else 10000
    t, l, b, r = bounds(coordinates)
    area = np.zeros((b - t + 1, r - l + 1))
    for y in range(t, b + 1):
        for x in range(l, r + 1):
            c = vicinity(x, y, coordinates)
            area[y - t][x - l] = c
    return np.sum(area < max_vicinity)
