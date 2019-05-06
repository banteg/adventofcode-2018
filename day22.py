from dataclasses import dataclass
from typing import Dict

import click
import networkx as nx

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
        self.erosion: Dict[Point, int] = {}

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


class RescueOperation(Grid):
    regions = ['rocky', 'wet', 'narrow']
    valid_tools = {
        'rocky': {'climbing gear', 'torch'},
        'wet': {'climbing gear', 'neither'},
        'narrow': {'torch', 'neither'},
    }

    def dijkstra(self, margin=20):
        G = nx.Graph()
        start = (self.mouth, 'torch')
        target = (self.target, 'torch')

        for x in range(self.target.x + margin):
            for y in range(self.target.y + margin):
                point = Point(x, y)

                # switch tool
                tool, other_tool = self.tools(point)
                G.add_edge((point, tool), (point, other_tool), weight=7)

                # move to adjacent region
                for dx, dy in [(1, 0), (0, 1)]:
                    move = point + Point(dx, dy)
                    for tool in self.tools(point) & self.tools(move):
                        G.add_edge((point, tool), (move, tool), weight=1)

        self.render(nx.dijkstra_path(G, start, target))
        return nx.dijkstra_path_length(G, start, target)

    def region(self, point):
        """Region type at coordinate."""
        return self.regions[self.erosion_level(point) % 3]

    def tools(self, point):
        """Tools usable at coordinate."""
        return self.valid_tools[self.region(point)]

    def render(self, path):
        path = {p: t for p, t in path}
        right = max(p.x for p in path)
        bottom = max(p.y for p in path)
        colors = {'neither': 'green', 'torch': 'yellow', 'climbing gear': 'red'}
        symbols = '.=|'
        for y in range(bottom + 1):
            for x in range(right + 1):
                p = Point(x, y)
                color = colors.get(path.get(p))
                symbol = symbols[self.erosion_level(p) % 3]
                click.secho(symbol, bg=color, dim=color is None, nl=False)
            print()


example = '''
    depth: 510
    target: 10,10
    '''


@aoc.test({example: 114})
def part_1(data: aoc.Data):
    a, b = data.ints_lines
    depth = a[0]
    target = Point(*b)
    return Grid(depth, target).survey()


@aoc.test({example: 45})
def part_2(data: aoc.Data):
    a, b = data.ints_lines
    depth = a[0]
    target = Point(*b)
    grid = RescueOperation(depth, target)
    grid.survey()
    return grid.dijkstra()
