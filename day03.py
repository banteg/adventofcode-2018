import aoc
import re
import numpy as np

@aoc.test({
'''#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2''': 4
})
def part_1(data):
    claims = [re.search(r'(\d+),(\d+): (\d+)x(\d+)', x) for x in data.splitlines()]
    rects = [tuple(map(int, x.groups())) for x in claims]
    fabric = np.zeros((1000, 1000))
    for x, y, w, h in rects:
        fabric[x:x+w, y:y+h] += 1
    return sum(sum(fabric > 1))


@aoc.test({
'''#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2''': 3
})
def part_1(data):
    claims = [re.search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', x) for x in data.splitlines()]
    rects = [tuple(map(int, x.groups())) for x in claims]
    fabric = np.zeros((1000, 1000))
    for n, x, y, w, h in rects:
        fabric[x:x+w, y:y+h] += 1
    for n, x, y, w, h in rects:
        if sum(sum(fabric[x:x+w, y:y+h] > 1)) == 0:
            return n
