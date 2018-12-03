import aoc
import numpy as np

@aoc.test({
'''#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2''': 4
})
def part_1(data: aoc.Data):
    rects = data.ints_lines
    fabric = np.zeros((1000, 1000))
    for n, x, y, w, h in rects:
        fabric[x:x+w, y:y+h] += 1
    return sum(sum(fabric > 1))


@aoc.test({
'''#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2''': 3
})
def part_1(data: aoc.Data):
    rects = data.ints_lines
    fabric = np.zeros((1000, 1000))
    for n, x, y, w, h in rects:
        fabric[x:x+w, y:y+h] += 1
    for n, x, y, w, h in rects:
        if sum(sum(fabric[x:x+w, y:y+h] > 1)) == 0:
            return n
