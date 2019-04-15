from collections import defaultdict, deque

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
    marbles = deque([0])
    hands = defaultdict(int)
    for marble in range(1, last + 1):
        if not marble % 23:
            hands[marble % players] += marble
            marbles.rotate(7)
            hands[marble % players] += marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(marble)
    return max(hands.values())


@aoc.test(examples)
def part_1(data: aoc.Data):
    players, last = data.ints_lines[0]
    return play_marbles(players, last)


@aoc.test({})
def part_2(data: aoc.Data):
    players, last = data.ints_lines[0]
    return play_marbles(players, last * 100)
