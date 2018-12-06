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
    x, y = np.array(coordinates).transpose()
    return y.min(), x.min(), y.max(), x.max()


def manhattan_distances(x, y, coordinates):
    return [abs(x - dx) + abs(y - dy) for dx, dy in coordinates]


def closest(x, y, coordinates):
    distances = manhattan_distances(x, y, coordinates)
    near = min(distances)
    if distances.count(near) > 1:
        return 0
    return distances.index(near) + 1


def vicinity(x, y, coordinates):
    distances = manhattan_distances(x, y, coordinates)
    return sum(distances)


@aoc.test({example: 17})
def part_1(data: aoc.Data):
    coordinates = data.ints_lines
    t, l, b, r = bounds(coordinates)
    area = np.zeros((b - t + 1, r - l + 1), int)
    for y in range(t, b + 1):
        for x in range(l, r + 1):
            c = closest(x, y, coordinates)
            area[y - t][x - l] = c
    # areas around borders are infinite
    infinite = set(area[0][:]) | set(area[-1][:]) | set(area[:][0]) | set(area[:][-1])
    areas = Counter(area.flatten()).most_common()
    non_infinite = [size for n, size in areas if n not in infinite]
    return non_infinite[0]


@aoc.test({example: 16})
def part_2(data: aoc.Data):
    coordinates = data.ints_lines
    t, l, b, r = bounds(coordinates)
    area = np.zeros((b - t + 1, r - l + 1), int)
    for y in range(t, b + 1):
        for x in range(l, r + 1):
            c = vicinity(x, y, coordinates)
            area[y - t][x - l] = c
    max_vicinity = 32 if data == example else 10000
    return np.sum(area < max_vicinity)
