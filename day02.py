from collections import Counter
from itertools import combinations
import aoc


@aoc.test({'abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab': 12})
def part_1(data: aoc.Data):
    counts = Counter()

    for line in data.splitlines():
        line_counts = Counter()
        for a, v in Counter(line).items():
            line_counts[v] = 1
        counts += line_counts

    return counts[2] * counts[3]


@aoc.test({'abcde\nfghij\nklmno\npqrst\nfguij\naxcye\nwvxyz': 'fgij'})
def part_2(data: aoc.Data):
    for p in combinations(data.splitlines(), 2):
        matching = [x for x, y in zip(*p) if x == y]
        distance = len(p[0]) - len(matching)
        if distance == 1:
            return ''.join(matching)
