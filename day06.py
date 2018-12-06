import aoc
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


def manhattan_distances(x, y, coordinates):
    return {
        c: abs(x - dx) + abs(y - dy)
        for c, (dx, dy) in enumerate(coordinates, 1)
    }


def closest(x, y, coordinates):
    distances = manhattan_distances(x, y, coordinates)
    n = min(distances, key=lambda k: distances[k])
    # equally distant locations are ignored
    if len([k for k in distances if distances[k] == distances[n]]) > 1:
        return 0
    return n


def vicinity(x, y, coordinates):
    distances = manhattan_distances(x, y, coordinates)
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
    areas = Counter(area.flatten()).most_common()
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
