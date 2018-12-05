from collections import deque
import aoc


def fold(polymer):
    units = {x.lower() for x in polymer}
    pairs = [u + u.upper() for u in units] + [u.upper() + u for u in units]
    size = 0
    while size != len(polymer):
        size = len(polymer)
        for reaction in pairs:
            polymer = polymer.replace(reaction, '')
    return polymer


@aoc.test({'dabAcCaCBAcCcaDA': 10})
def part_1(data: aoc.Data):
    return len(fold(data))


@aoc.test({'dabAcCaCBAcCcaDA': 4})
def part_2(data: aoc.Data):
    polymer = fold(data)
    units = {x.lower() for x in polymer}
    polymers = (polymer.replace(u, '').replace(u.upper(), '') for u in units)
    return min(len(fold(p)) for p in polymers)
