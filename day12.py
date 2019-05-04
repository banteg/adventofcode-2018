from collections import defaultdict
from itertools import count

import aoc


example = '''initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''


def print_state(state):
    pretty = ''.join(state.get(x, '.') for x in range(min(state), max(state) + 1))
    print(min(state), pretty, max(state))


def grow(state, notes):
    new = defaultdict(lambda: '.')
    for note in notes:
        rule, result = note.split(' => ')
        for i in range(min(state) - 2, max(state) + 3):
            pots = ''.join(state.get(x, '.') for x in range(i-2, i+3))
            if pots == rule:
                new[i] = result
    return new


def value(state):
    return sum(x for x in state if state[x] == '#')


@aoc.test({example: 325})
def part_1(data: aoc.Data):
    state, _, *notes = data.splitlines()
    state = dict(enumerate(state.split(': ')[-1]))
    for i in range(20):
        state = grow(state, notes)
    return value(state)


@aoc.test({})
def part_2(data: aoc.Data):
    state, _, *notes = data.splitlines()
    state = dict(enumerate(state.split(': ')[-1]))
    values = [value(state)]
    for gen in count(1):
        state = grow(state, notes)
        values.append(value(state))
        diffs = [v2 - v1 for v1, v2 in zip(values, values[1:])]
        if len(values) > 10 and len(set(diffs[-10:])) == 1:
            # found a stable point
            return (50000000000 - gen) * diffs[-1] + values[-1]
