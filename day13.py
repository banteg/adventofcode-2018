from collections import deque, defaultdict
from itertools import cycle

import click

import aoc

steps = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
}


class Car:

    def __init__(self, x, y, d):
        self.id = (x, y)
        self.x = x
        self.y = y
        self.alive = True
        self.facing = deque('^>v<')
        self.facing.rotate(-self.facing.index(d))
        self.r = 0
        self.actions = cycle(['left', 'straight', 'right'])

    def __repr__(self):
        return f'<Car {self.id} {self.x},{self.y} {self.d}>'

    @property
    def d(self):
        return self.facing[0]

    def look(self, grid):
        x, y = steps[self.d]
        return grid[self.y + y][self.x + x]

    def move(self):
        dx, dy = steps[self.d]
        self.x += dx
        self.y += dy

    def turn(self, where):
        direction = {'left': 1, 'right': -1}
        self.facing.rotate(direction.get(where, 0))

    def turn_direction(self, n):
        if (self.d in '<>' and n == '/') or (self.d in '^v' and n == '\\'):
            self.turn('left')
        else:
            self.turn('right')

    def tick(self, n):
        self.move()
        if n == '+':
            act = next(self.actions)
            self.turn(act)
            self.r += 1
        elif n in '/\\':
            self.turn_direction(n)


def render(grid, cars):
    msg = []
    car_coords = {(c.x, c.y): c for c in cars}
    for y, row in enumerate(grid):
        msg.append(f'{y:4d} ')
        for x, g in enumerate(row):
            if (x, y) in car_coords:
                msg.append(click.style(car_coords[(x, y)].d, bold=True, fg='green' if car_coords[(x, y)].alive else 'red'))
            else:
                msg.append(click.style(g, dim=True))
        msg.append('\n')
    print(''.join(msg))


def detect_crash(cars):
    alive = [c for c in cars if c.alive]
    coords = defaultdict(list)
    for c in alive:
        coords[(c.x, c.y)].append(c)

    crashed = [i for i in coords if len(coords[i]) > 1]
    for i in crashed:
        # print('crash at', i, coords[i])
        for c in coords[i]:
            c.alive = False

    if crashed:
        x, y = crashed[0]
        return f'{x},{y}'


def move(grid, cars):
    for car in sorted(cars, key=lambda c: (c.y, c.x)):
        car.tick(car.look(grid))
        crashed = detect_crash(cars)
        if crashed:
            return crashed


def load_cars(grid):
    cars = []
    for y, row in enumerate(grid):
        for x, car in enumerate(row):
            if car in '^v<>':
                cars.append(Car(x, y, car))
    return cars


def recover_tracks(data):
    tracks = {
        '>': '-',
        '<': '-',
        '^': '|',
        'v': '|',
    }
    for car in tracks:
        data = data.replace(car, tracks[car])
    return data.splitlines()


def eliminate(grid, cars):
    for car in sorted(cars, key=lambda c: (c.y, c.x)):
        if car.alive:
            car.tick(car.look(grid))
            crashed = detect_crash(cars)
            # if crashed:
            #     render(grid, cars)


@aoc.test({})
def part_1(data: aoc.Data):
    grid = data.splitlines()
    cars = load_cars(grid)

    grid = recover_tracks(data)
    crashed = False
    while not crashed:
        crashed = move(grid, cars)
    return crashed


@aoc.test({})
def part_2(data: aoc.Data):
    grid = data.splitlines()
    cars = load_cars(grid)

    grid = recover_tracks(data)
    while True:
        crashed = eliminate(grid, cars)
        alive = [x for x in cars if x.alive]
        if len(alive) == 1:
            return f'{alive[0].x},{alive[0].y}'
