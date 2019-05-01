from collections import deque
from dataclasses import dataclass


import aoc

import click


@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


moves = {
    'N': Point(0, -1),
    'S': Point(0, 1),
    'W': Point(-1, 0),
    'E': Point(1, 0),
}

doors = {
    'N': '-',
    'S': '-',
    'W': '|',
    'E': '|',
}


@dataclass
class Grid:
    grid: dict

    def __repr__(self):
        ax = min(p.x for p in self.grid) - 1
        ay = min(p.y for p in self.grid) - 1
        bx = max(p.x for p in self.grid) + 1
        by = max(p.y for p in self.grid) + 1
        msg = ''
        for y in range(ay, by + 1):
            for x in range(ax, bx + 1):
                if x in (ax, bx) and y in (ay, by):
                    msg += '#'  # draw outer walls
                else:
                    msg += self.grid.get(Point(x, y), '#')
            msg += '\n'
        return msg

    @classmethod
    def from_string(cls, data):
        g = cls({})
        pos = Point()
        g.grid[pos] = 'X'
        stack = []
        starts = {}
        for i, symbol in enumerate(data):
            if symbol in '^$':
                continue
            elif symbol in moves:
                # create a door and a room
                pos += moves[symbol]
                g.grid[pos] = doors[symbol]
                pos += moves[symbol]
                g.grid[pos] = '.'
            elif symbol in '^(':
                # remember where the group starts
                stack.append(i)
                starts[i] = pos
            elif symbol in ')$':
                # close the innermost group
                stack.pop()
            elif symbol == '|':
                # return to the inner group start pos
                pos = starts[stack[-1]]
            else:
                raise ValueError(symbol)
        return g

    def find_room_distances(self):
        start = Point()
        visited = {start}
        frontier = [(0, start)]
        dists = {start: 0}
        while frontier:
            dist, pos = frontier.pop(0)
            for n in self.neighbours(pos):
                if n in visited:
                    continue
                if n not in dists or dists[n] > dist + 1:
                    dists[n] = dist + 1
                visited.add(n)
                frontier.append((dist + 1, n))
        return dists

    def neighbours(self, point):
        return [
            point + move + move for move in moves.values()
            if self.grid.get(point + move) in doors.values()
        ]

examples = {
    '^WNE$': 3,
    '^N(E|W)S$': 3,
    '^N(EEENWWW|N)$': 5,
    '^(SENNWWSWN|WSW)$': 4,
    '^ENWWW(NEEE|SSE(EE|N))$': 10,
    '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$': 18,
    '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$': 23,
    '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$': 31,
}

@aoc.test(examples)
def part_1(data: aoc.Data):
    grid = Grid.from_string(data.strip())
    # print(grid)
    return max(grid.find_room_distances().values())


@aoc.test({})
def part_2(data: aoc.Data):
    grid = Grid.from_string(data.strip())
    dist = grid.find_room_distances()
    return len([x for x in dist.values() if x >= 1000])
