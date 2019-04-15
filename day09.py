from collections import defaultdict
from itertools import count

import aoc


examples = {
    '9 players; last marble is worth 25 points': 32,
    '10 players; last marble is worth 1618 points': 8317,
    '13 players; last marble is worth 7999 points': 146373,
    '17 players; last marble is worth 1104 points': 2764,
    '21 players; last marble is worth 6111 points': 54718,
    '30 players; last marble is worth 5807 points': 37305,
}


def play_marbles(players, last):
    marbles = [0]
    hands = defaultdict(set)
    upcoming = count(1)
    pos = 0
    for i in range(1, last + 1):
        marble = next(upcoming)
        if not marble % 23:
            hands[i % players].add(marble)
            pos = (pos - 7) % len(marbles)
            hands[i % players].add(marbles.pop(pos))
        else:
            pos = (pos + 2) % len(marbles)
            marbles.insert(pos, marble)
    return max(sum(hand) for hand in hands.values())


@aoc.test(examples)
def part_1(data: aoc.Data):
    players, last = data.ints_lines[0]
    return play_marbles(players, last)
