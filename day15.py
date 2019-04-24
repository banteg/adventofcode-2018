from collections import deque
from dataclasses import dataclass
from heapq import heappush, heappop
from itertools import chain
from time import time

import numpy as np
import pyglet
from PIL import Image
from pyglet.gl import *

import aoc

examples = {
'''\
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######''': 36334,

'''\
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######''': 39514,

'''\
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######''': 27755,

'''\
#######   
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######''': 28944,

'''\
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########''': 18740,
}

examples = {
'''\
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########''': 1
}


'''
Here's a few examples that will fail for common errors on this problem:
#######
#######
#.E..G#
#.#####
#G#####
#######
#######
In this first case, the Elf should move to the right.
####
#GG#
#.E#
####
With this input, the elf should begin by attacking the goblin directly above him.
#######
#######
#####G#
#..E..#
#G#####
#######
#######
For this input, the elf should move to the left.
'''


window = pyglet.window.Window(500, 500, caption='aoc 2018 day 15')


def took(f):
    def decorator(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        print(f'{f.__name__} took {time() - start:.3f}s')
        return result

    return decorator


def flat(it):
    return list(chain.from_iterable(it))


@dataclass
class Point:
    x: int
    y: int

    @property
    def neighbours(self):
        return [self + delta for delta in [Point(0, -1), Point(-1, 0), Point(1, 0), Point(0, 1)]]

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Unit:
    pos: Point
    symbol: str
    hp: int = 200
    dmg: int = 3

    @property
    def alive(self):
        return self.hp > 0

    def __repr__(self):
        return f'<{self.symbol} ({self.pos}) {self.hp} hp>'

    def __hash__(self):
        return hash((self.pos, self.symbol, self.hp, self.dmg))


def reading_order(p):
    if isinstance(p, Unit):
        p = p.pos
    return p.y, p.x


class Simulation:

    def __init__(self, data):
        self.units = set()
        self.walls = set()
        for y, row in enumerate(data.splitlines()):
            for x, symbol in enumerate(row):
                if symbol == '#':
                    self.walls.add(Point(x, y))
                if symbol in 'EG':
                    self.units.add(Unit(Point(x, y), symbol))
        self.bounds = x, y
        self.rounds = 0

    def run(self):
        self.render_gl()
        while True:
            result = self.tick()
            if result:
                return result

    @property
    def has_ended(self):
        return len({x.symbol for x in self.units if x.alive}) == 1

    def is_wall(self, pos):
        walls = self.walls | {unit.pos for unit in self.units if unit.alive}
        return pos in walls

    def passable(self, points):
        return [point for point in points if not self.is_wall(point)]

    # @took
    def tick(self):
        self.render_gl()
        # print(f'--tick {self.rounds}--')
        for i, unit in enumerate(sorted(self.units, key=reading_order)):
            if self.has_ended:
                winners = {x.symbol for x in self.units if x.alive}.pop()
                winning_hp = sum(unit.hp for unit in self.units if unit.alive and unit.symbol == winners)
                print(self.rounds, winning_hp)
                return self.rounds * winning_hp

            if not unit.alive:
                continue
            # print(f'({i+1}/{len(self.units)}) {unit}')
            targets = [x for x in self.units if unit.symbol != x.symbol and x.alive]

            # attack if in range
            melee = [x for x in targets if x.pos in unit.pos.neighbours]
            if melee:
                target = sorted(melee, key=reading_order)[0]
                target.hp -= unit.dmg
                # print(f'attack {target}')
                continue

            # walk towards nearest target
            in_range = flat(self.passable(t.pos.neighbours) for t in targets)

            came_from = self.breadth_search(unit.pos)

            paths = [self.reconstruct_path(came_from, g) for g in in_range]
            print(paths)

            if unit.symbol == 'E':
                print('xx', [p for p in paths if p[-1] == (4, 3)])
                self.render_gl(in_range)
                input()

            scores = [(len(path), path[1]) for path in paths if path and len(path) > 1]
            ways = {p for s, p in scores}
            print(ways)
            sco = {w: min(s for s, p in scores if w == p) for w in ways}
            print('sco', sco)
            # grid = [Point(x, y) for x in range(self.bounds[0]) for y in range(self.bounds[1])]
            # sco = {p: self.reconstruct_path(came_from, p) for p in grid}
            # sco = {p: len(sco[p]) for p in sco if sco[p]}
            # print(sco)
            self.render_gl(scores=sco, coords=True)
            # input()
            if scores:
                print(sorted(scores))
                best = min(s for s, p in scores)
                print(unit, sorted(p for s, p in scores if s == best))
                unit.pos = sorted(scores)[0][1]
                continue
        self.rounds += 1

    def breadth_search(self, start: Point):
        frontier = deque([start])
        visited = {start}
        came_from = {start: None}
        while frontier:
            pos = frontier.popleft()
            for n in self.passable(pos.neighbours):
                if n not in came_from:
                    came_from[n] = pos
                if n not in visited:
                    frontier.append(n)
                    visited.add(n)
            self.render_gl(visited, frontier)
        return came_from

    def reconstruct_path(self, came_from, goal):
        if goal not in came_from:
            return None
        path = []
        c = came_from[goal]
        while c:
            path.insert(0, c)
            c = came_from[c]
        return path

    def render_gl(self, red=None, yellow=None, scores=None, coords=False):
        colors = {
            'G': [163, 190, 140],
            'E': [180, 142, 173],
            '.': [236, 239, 244],
            '#': [59, 66, 82],
            '!': [191, 97, 106],
            '@': [235, 203, 139],
        }
        w, h = self.bounds
        data = [['.' for x in range(w + 1)] for y in range(h + 1)]
        for wall in self.walls:
            data[wall.y][wall.x] = '#'
        for p in red or []:
            data[p.y][p.x] = '!'
        for p in yellow or []:
            data[p.y][p.x] = '@'
        for unit in self.units:
            data[unit.pos.y][unit.pos.x] = unit.symbol

        col = [[colors[x] for x in row] for row in data]
        arr = np.array(col)
        arr = np.flip(arr, 0)
        img = Image.fromarray(arr.astype(np.uint8))
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

        # render text
        for unit in self.units:
            label = pyglet.text.Label(
                f'{unit.hp}',
                font_name='Helvetica',
                font_size=8,
                x=unit.pos.x * scale + scale / 2,
                y=window.height - unit.pos.y * scale - scale / 2,
                anchor_x='center', anchor_y='center', color=(236, 239, 244, 255),
            )
            label.draw()

        # coords
        if coords:
            for x in range(w + 1):
                for y in range(h + 1):
                    label = pyglet.text.Label(
                        f'{x},{y}',
                        font_name='Helvetica',
                        font_size=8,
                        x=x * scale + scale / 2,
                        y=window.height - y * scale - scale,
                        anchor_x='center', anchor_y='bottom', color=(0, 0, 0, 255),
                    )
                    label.draw()

        if scores:
            for p in scores:
                label = pyglet.text.Label(
                    f'{scores[p]}',
                    font_name='Helvetica',
                    font_size=12,
                    x=p.x * scale + scale / 2,
                    y=window.height - p.y * scale - scale / 2,
                    anchor_x='center', anchor_y='center', color=(0, 0, 200, 255),
                )
                label.draw()

        # round
        label = pyglet.text.Label(
            f'round {self.rounds}',
            font_name='Helvetica',
            font_size=12,
            x=window.width / 2,
            y=window.height - scale / 2,
            anchor_x='center', anchor_y='center',
            color=(236, 239, 244, 255),
        )
        label.draw()

        window.flip()


@aoc.test(examples)
def part_1(data: aoc.Data):
    sim = Simulation(data)
    return sim.run()
