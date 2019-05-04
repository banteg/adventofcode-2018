from itertools import count
import numpy as np
from matplotlib.pyplot import imshow, show

import aoc

example = '''
    position=< 9,  1> velocity=< 0,  2>
    position=< 7,  0> velocity=<-1,  0>
    position=< 3, -2> velocity=<-1,  1>
    position=< 6, 10> velocity=<-2, -1>
    position=< 2, -4> velocity=< 2,  2>
    position=<-6, 10> velocity=< 2, -2>
    position=< 1,  8> velocity=< 1, -1>
    position=< 1,  7> velocity=< 1,  0>
    position=<-3, 11> velocity=< 1, -2>
    position=< 7,  6> velocity=<-1, -1>
    position=<-2,  3> velocity=< 1,  0>
    position=<-4,  3> velocity=< 2,  0>
    position=<10, -3> velocity=<-1,  1>
    position=< 5, 11> velocity=< 1, -2>
    position=< 4,  7> velocity=< 0, -1>
    position=< 8, -2> velocity=< 0,  1>
    position=<15,  0> velocity=<-2,  0>
    position=< 1,  6> velocity=< 1,  0>
    position=< 8,  9> velocity=< 0, -1>
    position=< 3,  3> velocity=<-1,  1>
    position=< 0,  5> velocity=< 0, -1>
    position=<-2,  2> velocity=< 2,  0>
    position=< 5, -2> velocity=< 1,  2>
    position=< 1,  4> velocity=< 2,  1>
    position=<-2,  7> velocity=< 2, -2>
    position=< 3,  6> velocity=<-1, -1>
    position=< 5,  0> velocity=< 1,  0>
    position=<-6,  0> velocity=< 2,  0>
    position=< 5,  9> velocity=< 1, -2>
    position=<14,  7> velocity=<-2,  0>
    position=<-3,  6> velocity=< 2, -1>
    '''


def step(points):
    return [[x + xv, y + yv, xv, yv] for x, y, xv, yv in points]


def bounds(points):
    return [
        min(x for x, y, *_ in points), max(x for x, y, *_ in points),
        min(y for x, y, *_ in points), max(y for x, y, *_ in points),
    ]


def area(points):
    xa, xb, ya, yb = bounds(points)
    return (xb - xa) * (yb - ya)


def as_array(points):
    xa, xb, ya, yb = bounds(points)
    canvas = np.zeros((yb - ya + 1, xb - xa + 1))
    for x, y, *_ in points:
        canvas[y - ya][x - xa] = 1
    return canvas


def ocr(points):
    # detect full-height vertical lines
    arr = as_array(points)
    return sum(sum(arr) == arr.shape[0])


def render(points):
    canvas = as_array(points)
    imshow(canvas)
    show()


@aoc.test({example: 3})
def part_1_2(data: aoc.Data):
    points = data.ints_lines
    for t in count(1):
        points = step(points)
        a = area(points)
        if a < 10000 and ocr(points):
            render(points)
            return t
