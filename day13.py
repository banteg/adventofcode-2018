from collections import deque, Counter
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
        self.x = x
        self.y = y
        self.alive = True
        self.facing = deque('^>v<')
        self.facing.rotate(-self.facing.index(d))
        self.r = 0
        self.actions = cycle(['left', 'straight', 'right'])

    def __repr__(self):
        return f'<Car {self.x},{self.y} {self.d}>'

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
        msg += f'{y:4d}'
        for x, g in enumerate(row):
            if (x, y) in car_coords:
                msg.append(click.style(car_coords[(x, y)].d, bold=True, fg='green'))
            else:
                msg.append(click.style(g, dim=True))
        msg.append('\n')
    print(''.join(msg))
    input()


def detect_crash(cars):
    (x, y), count = Counter((c.x, c.y) for c in cars).most_common()[0]
    if count > 1:
        return f'{x},{y}'


def move(grid, cars):
    for car in sorted(cars, key=lambda c: (c.y, c.x)):
        car.tick(car.look(grid))
        crashed = detect_crash(cars)
        if crashed:
            return crashed
    # render(grid, cars)


@aoc.test({})
def part_1(data: aoc.Data):
    # get car locations
    grid = data.splitlines()
    cars = []
    for y, row in enumerate(grid):
        for x, car in enumerate(row):
            if car in '^v<>':
                cars.append(Car(x, y, car))

    # recover tracks
    tracks = {
        '>': '-',
        '<': '-',
        '^': '|',
        'v': '|',
    }
    grid = data.translate(str.maketrans(tracks)).splitlines()
    crashed = False
    while not crashed:
        crashed = move(grid, cars)
    return crashed
