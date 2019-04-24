from collections import deque
from dataclasses import dataclass
from itertools import chain, count

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
        walls = set()
        units = []  # units are mutable, so hashing is unsafe
        for y, row in enumerate(data):
            for x, symbol in enumerate(row):
                if symbol == '#':
                    walls.add(Point(x, y))
                if symbol in 'EG':
                    units.append(Unit(Point(x, y), symbol))
        self = cls(walls, units)
        self.dimensions = Point(x, y)
        self.update_passable_cache()
        return self

    @property
    def turn_order(self) -> [Unit]:
        return sorted(self.alive_units, key=reading_order)

    @property
    def alive_units(self) -> [Unit]:
        return [x for x in self.units if x.alive]

    def move(self, unit: Unit):
        '''unit can either 1) attack or 2) move then attack'''
        if not unit.alive:
            return
        attacked = self.melee(unit)
        if attacked:
            return  # end turn
        moved = self.find_move(unit)
        if moved:
            self.melee(unit)

    def melee(self, unit: Unit):
        '''choose nearest unit with the lowest hp'''
        targets = [x for x in unit.targets(self.alive_units) if x in unit.near]
        try:
            fewest_hp = min(x.hp for x in targets)
        except ValueError:
            return
        tied = [x for x in targets if x.hp == fewest_hp]
        target = sorted(tied, key=reading_order)[0]
        unit.attack(target)
        if target.hp <= 0:
            self.update_passable_cache()
        return True

    def find_move(self, unit):
        targets = flat(target.near for target in unit.targets(self.units))
        chosen = self.breadth_search(unit.pos, self.passable(targets))
        if chosen:
            unit.pos = chosen
            self.update_passable_cache()
            return True

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
        chosen = nearest[0]
        while meta[chosen][0] > 1:
            chosen = meta[chosen][1]
        return chosen

    def update_passable_cache(self):
        units = {unit.pos for unit in self.alive_units}
        self.cant_pass = self.walls | units

    def passable(self, points):
        '''filter passable points using cache'''
        return [point for point in points if point not in self.cant_pass]

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
            if verbose:
                print(f'After {self.rounds} rounds:')
                self.grid.render()

    def tick(self):
        turns = len(self.grid.turn_order)
        for i, unit in enumerate(self.grid.turn_order):
            self.grid.move(unit)
            if i == turns - 1:
                self.rounds += 1
            outcome = self.check_outcome()
            if outcome:
                return outcome

    def check_outcome(self):
        factions = {x.symbol for x in self.grid.alive_units}
        if len(factions) == 1:
            winners = factions.pop()
            hp = sum(unit.hp for unit in self.grid.alive_units if unit.symbol == winners)
            return hp * self.rounds


class ElfDied(Exception):
    pass


@dataclass
class Simulation2:
    data: str
    rounds: int = 0

    def run(self, verbose=True):
        for dmg in count(4):
            print(f'checking damage = {dmg}')
            self.rounds = 0
            self.grid = Grid.from_string(self.data)
            self.elves = [x for x in self.grid.units if x.symbol == 'E']
            for unit in self.elves:
                unit.dmg = dmg
            # run2
            if verbose:
                print('Initially:')
                self.grid.render()
            elves_ok = True
            while elves_ok:
                try:
                    outcome = self.tick()
                except ElfDied:
                    print('elf died, trying next...')
                    elves_ok = False
                    continue
                if outcome:
                    if verbose:
                        print(f'Outcome:')
                        self.grid.render()
                    return outcome
                if verbose:
                    print(f'After {self.rounds} rounds:')
                    self.grid.render()

    def tick(self):
        turns = len(self.grid.turn_order)
        for i, unit in enumerate(self.grid.turn_order):
            self.grid.move(unit)
            if i == turns - 1:
                self.rounds += 1
            outcome = self.check_outcome()
            if outcome:
                return outcome

    def check_outcome(self):
        elves_alive = all(x.alive for x in self.elves)
        if not elves_alive:
            raise ElfDied()
        others_dead = not any(x.alive for x in self.grid.units if x.symbol != 'E')
        if elves_alive and others_dead:
            hp = sum(unit.hp for unit in self.elves)
            print(f'hp={hp}, rounds={self.rounds}')
            return hp * self.rounds


@aoc.test(examples)
def part_1(data: aoc.Data):
    sim = Simulation(Grid.from_string(data))
    return sim.run(verbose=True)


examples2 = {
    '#######\n#.G...#\n#...EG#\n#.#.#G#\n#..G#E#\n#.....#\n#######': 4988,
    '#######\n#E..EG#\n#.#G.E#\n#E.##E#\n#G..#.#\n#..E#.#\n#######': 31284,
    '#######\n#E.G#.#\n#.#G..#\n#G.#.G#\n#G..#.#\n#...E.#\n#######': 3478,
    '#######\n#.E...#\n#.#..G#\n#.###.#\n#E#G#G#\n#...#G#\n#######': 6474,
    '#########\n#G......#\n#.E.#...#\n#..##..G#\n#...##..#\n#...#...#\n#.G...G.#\n#.....G.#\n#########': 1140,
}

@aoc.test(examples2)
def part_2(data: aoc.Data):
    sim = Simulation2(data)
    return sim.run(verbose=True)
