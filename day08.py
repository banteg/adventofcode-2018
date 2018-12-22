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


def node_value(data):
    children = next(data)
    metadata = next(data)
    values = []
    for i in range(children):
        values.append(node_value(data))
    metas = []
    for i in range(metadata):
        metas.append(next(data))
    if children:
        total = sum(values[index - 1] for index in metas if index - 1 < len(values))
    else:
        total = sum(metas)
    return total


@aoc.test({example: 138})
def part_1(data: aoc.Data):
    numbers = data.ints_lines[0]
    return load_node(iter(numbers))


@aoc.test({example: 66})
def part_2(data: aoc.Data):
    numbers = data.ints_lines[0]
    return node_value(iter(numbers))
