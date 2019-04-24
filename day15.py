from collections import deque
from dataclasses import dataclass
from itertools import chain

import aoc

examples = {
    '#######\n#G..#E#\n#E#E.E#\n#G.##.#\n#...#E#\n#...E.#\n#######': 36334,
    '#######\n#E..EG#\n#.#G.E#\n#E.##E#\n#G..#.#\n#..E#.#\n#######': 39514,
    '#######\n#E.G#.#\n#.#G..#\n#G.#.G#\n#G..#.#\n#...E.#\n#######': 27755,
    '#######   \n#.E...#\n#.#..G#\n#.###.#\n#E#G#G#\n#...#G#\n#######': 28944,
    '#########\n#G......#\n#.E.#...#\n#..##..G#\n#...##..#\n#...#...#\n#.G...G.#\n#.....G.#\n#########': 18740
}


def reading_order(point):
    return point.y, point.x


def flat(it):
    return list(chain.from_iterable(it))


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def near(self):
        return [
            self + Point(0, -1),
            self + Point(-1, 0),
            self + Point(1, 0),
            self + Point(0, 1),
        ]


@dataclass
class Unit:
    pos: Point
    symbol: str
    hp: int = 200
    dmg: int = 3

    def __getattr__(self, item):
        return getattr(self.pos, item)

    @property
    def alive(self):
        return self.hp > 0

    def foe(self, other):
        return self.symbol != other.symbol

    def attack(self, other):
        other.hp -= self.dmg

    def targets(self, others):
        return [x for x in others if self.foe(x) and x.alive]


@dataclass
class Grid:
    walls: [Point]
    units: [Unit]

    @classmethod
    def from_string(cls, data):
        if isinstance(data, str):
            data = data.splitlines()
        walls, units = [], []
        for y, row in enumerate(data):
            for x, symbol in enumerate(row):
                if symbol == '#':
                    walls.append(Point(x, y))
                if symbol in 'EG':
                    units.append(Unit(Point(x, y), symbol))
        self = cls(walls, units)
        self.dimensions = Point(x, y)
        return self

    @property
    def turn_order(self) -> [Unit]:
        return sorted(self.alive_units, key=reading_order)

    @property
    def alive_units(self) -> [Unit]:
        return [x for x in self.units if x.alive]

    def move(self, unit: Unit):
        # 1. attack if in range
        target = self.melee(unit)
        if target is not None:
            unit.attack(target)
            return  # end turn
        # 2. move if possible
        targets = unit.targets(self.units)
        poi = flat(self.passable(target.near) for target in targets)
        chosen = self.breadth_search(unit.pos, poi)
        if chosen:
            unit.pos = chosen
        # melee attack
        if chosen:
            target = self.melee(unit)
            if target is not None:
                unit.attack(target)

    def melee(self, unit: Unit):
        '''choose nearest unit with the lowest hp'''
        targets = [x for x in unit.targets(self.alive_units) if x in unit.near]
        try:
            fewest_hp = min(x.hp for x in targets)
        except ValueError:
            return
        chosen = [x for x in targets if x.hp == fewest_hp]
        return sorted(chosen, key=reading_order)[0]

    def breadth_search(self, start: Point, targets: [Point]):
        frontier = deque([(0, start)])  # dist, pos
        visited = {start}
        meta = {start: (0, None)}  # dist, came_from
        while frontier:
            dist, pos = frontier.popleft()
            for n in self.passable(pos.near):
                if n in visited:
                    continue
                if n not in meta or meta[n] > (dist + 1, pos):
                    if n in meta and meta[n] > (dist + 1, pos):
                        print(f'n={n} added to meta ({dist + 1}, {pos}), was {meta.get(n)}')
                    meta[n] = dist + 1, pos
                visited.add(n)
                frontier.append((dist + 1, n))

        reachable = [(dist, pos) for pos, (dist, _) in meta.items() if pos in targets]
        try:
            min_dist = min(dist for dist, pos in reachable)
        except ValueError:
            return
        closest = [pos for dist, pos in reachable if dist == min_dist]
        nearest = sorted(closest, key=reading_order)
        # start debug
        debug_cost = {p: str(dist) for p, (dist, _) in meta.items()}
        debug_near = {p: '!' for p in nearest}
        #         self.render({**debug_cost, **debug_near})
        # end debug
        chosen = nearest[0]
        while meta[chosen][0] > 1:
            chosen = meta[chosen][1]
        return chosen

    def passable(self, points):
        return [point for point in points if point not in self.walls + self.alive_units]

    def locate(self, point):
        if point in self.walls:
            return '#'
        units = {unit.pos: unit for unit in self.alive_units}
        if point in units:
            return units[point].symbol
        return '.'

    def render(self, extra=None):
        extra = {} if extra is None else extra
        msg = ''
        hp = []
        for y in range(self.dimensions.y + 1):
            hp = [f'{unit.symbol}({unit.hp})' for unit in sorted(self.alive_units, key=reading_order) if unit.y == y]
            for x in range(self.dimensions.x + 1):
                point = Point(x, y)
                msg += extra.get(point, self.locate(point))
            msg += '  ' + ', '.join(hp)
            msg += '\n'
        print(msg)


@dataclass
class Simulation:
    grid: Grid
    rounds: int = 0

    def run(self, verbose=False):
        if verbose:
            print('Initially:')
            self.grid.render()
        while True:
            outcome = self.tick()
            if outcome:
                if verbose:
                    print(f'Outcome:')
                    self.grid.render()
                return outcome
            self.rounds += 1
            if verbose:
                print(f'After {self.rounds} rounds:')
                self.grid.render()

    def tick(self):
        for unit in self.grid.turn_order:
            if not unit.alive:
                continue
            self.grid.move(unit)
            outcome = self.check_outcome()
            if outcome:
                return outcome

    def check_outcome(self):
        factions = {x.symbol for x in self.grid.alive_units}
        if len(factions) == 1:
            winners = factions.pop()
            print([unit.hp for unit in self.grid.alive_units])
            hp = sum(unit.hp for unit in self.grid.alive_units if unit.symbol == winners)
            print(f'outcome: rounds={self.rounds}, hp={hp}')
            return hp * self.rounds


@aoc.test(examples)
def part_1(data: aoc.Data):
    sim = Simulation(Grid.from_string(data))
    return sim.run(verbose=True)
