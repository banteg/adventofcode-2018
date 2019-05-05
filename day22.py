from dataclasses import dataclass

import aoc


@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Grid:

    def __init__(self, depth: int, target: Point):
        self.mouth = Point(0, 0)
        self.depth = depth
        self.target = target
        self.erosion = {}

    def survey(self):
        return sum(self.erosion_level(point) % 3 for point in self.walk())

    def walk(self):
        for y in range(self.target.y + 1):
            for x in range(self.target.x + 1):
                yield Point(x, y)

    def geologic_index(self, point: Point):
        if point in [self.mouth, self.target]:
            return 0
        if point.y == 0:
            return point.x * 16807
        if point.x == 0:
            return point.y * 48271
        left = point + Point(-1, 0)
        top = point + Point(0, -1)
        return self.erosion_level(left) * self.erosion_level(top)

    def erosion_level(self, point: Point):
        if point not in self.erosion:
            self.erosion[point] = (self.geologic_index(point) + self.depth) % 20183
        return self.erosion[point]


examples = {
    '''
    depth: 510
    target: 10,10
    ''': 114
}


@aoc.test(examples)
def part_1(data: aoc.Data):
    a, b = data.ints_lines
    depth = a[0]
    target = Point(*b)
    return Grid(depth, target).survey()
