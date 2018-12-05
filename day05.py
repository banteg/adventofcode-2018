import aoc


def fold(polymer):
    while True:
        reactions = []
        i = 0
        while i < len(polymer) - 2:
            a, b = sorted(polymer[i:i+2])
            if a.lower() == b.lower() and a.isupper() and b.islower():
                reactions.append(i)
                i += 2
            else:
                i += 1

        for c, i in enumerate(reactions):
            polymer = polymer[:i-c*2] + polymer[i-c*2+2:]

        if not reactions:
            return polymer


@aoc.test({'dabAcCaCBAcCcaDA': 10})
def part_1(data: aoc.Data):
    return len(fold(data))


@aoc.test({'dabAcCaCBAcCcaDA': 4})
def part_2(data: aoc.Data):
    polymer = fold(data)
    units = {x.lower() for x in polymer}
    polymers = (polymer.replace(u, '').replace(u.upper(), '') for u in units)
    return min(len(fold(p)) for p in polymers)
