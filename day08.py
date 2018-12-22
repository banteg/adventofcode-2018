import aoc
from collections import defaultdict


example = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'


def load_node(data):
    total = 0
    children = next(data)
    metadata = next(data)
    for i in range(children):
        total += load_node(data)
    for i in range(metadata):
        total += next(data)
    return total


@aoc.test({example: 138})
def part_1(data: aoc.Data):
    numbers = data.ints_lines[0]
    return load_node(iter(numbers))
