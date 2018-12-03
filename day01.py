from itertools import cycle
import aoc


@aoc.test({
    '+1\n-2\n+3\n+1': 3,
    '+1\n+1\n+1': 3,
    '+1\n+1\n-2': 0,
    '-1\n-2\n-3': -6,
})
def part_1(data):
    value = 0
    for adj in data.splitlines():
        value += int(adj)
    return value


@aoc.test({
    '+1\n-2\n+3\n+1': 2,
    '+1\n-1': 0,
    '+3\n+3\n+4\n-2\n-4': 10,
    '-6\n+3\n+8\n+5\n-6': 5,
    '+7\n+7\n-2\n-7\n-4': 14,
})
def part_2(data):
    value = 0
    seen = {0}
    for adj in cycle(data.splitlines()):
        value += int(adj)
        if value in seen:
            break
        seen.add(value)
    return value
