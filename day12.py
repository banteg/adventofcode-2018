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


def grow(state, notes):
    new = {x: '.' for x in state}
    for note in notes:
        rule, result = note.split(' => ')
        for i in range(min(state) + 2, max(state) - 2):
            pots = ''.join(state[x] for x in range(i-2, i+3))
            if pots == rule:
                new[i] = result
    return new


@aoc.test({example: 325})
def part_1(data: aoc.Data):
    state, _, *notes = data.splitlines()
    state = dict(enumerate(state.split(': ')[-1]))
    state = {x: state.get(x, '.') for x in range(-40, len(state) + 42)}
    for i in range(20):
        state = grow(state, notes)
    return sum(x for x in state if state[x] == '#')
