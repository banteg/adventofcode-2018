import aoc

def fold(polymer):
    while True:
        reactions = []
        scan = iter(range(len(polymer) - 1))

        for i in scan:
            a, b = sorted(polymer[i:i+2])
            same_unit = a.lower() == b.lower()
            different_polarity = a.isupper() and b.islower()
            if same_unit and different_polarity:
                reactions.append(i)
                next(scan)  # skip next to avoid 'aAa' situation
        
        for c, i in enumerate(reactions):
            polymer = polymer[:i-c*2] + polymer[i-c*2+2:]

        if not reactions:
            return polymer


@aoc.test({'dabAcCaCBAcCcaDA': 10})
def part_1(data: aoc.Data):
    return len(fold(data))
