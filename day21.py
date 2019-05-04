import aoc


codes = {
    'addr': lambda r, a, b: r[a] + r[b],
    'addi': lambda r, a, b: r[a] + b,
    'mulr': lambda r, a, b: r[a] * r[b],
    'muli': lambda r, a, b: r[a] * b,
    'banr': lambda r, a, b: r[a] & r[b],
    'bani': lambda r, a, b: r[a] & b,
    'borr': lambda r, a, b: r[a] | r[b],
    'bori': lambda r, a, b: r[a] | b,
    'setr': lambda r, a, b: r[a],
    'seti': lambda r, a, b: a,
    'gtir': lambda r, a, b: int(a > r[b]),
    'grti': lambda r, a, b: int(r[a] > b),
    'gtrr': lambda r, a, b: int(r[a] > r[b]),
    'eqir': lambda r, a, b: int(a == r[b]),
    'eqri': lambda r, a, b: int(r[a] == b),
    'eqrr': lambda r, a, b: int(r[a] == r[b]),
}


def run_program(code, part=1):
    r = [0, 0, 0, 0, 0, 0]
    ipr, *program = code.splitlines()
    ipr = int(ipr.split()[1])
    lines = dict(enumerate(program))
    ip = 0
    while True:
        i, *args = lines[ip].split()
        a, b, c = map(int, args)
        r[ipr] = ip

        # addi 2 1 2
        if ip == 24:
            r[2] = r[3] // 256
        else:
            r[c] = codes[i](r, a, b)

        # eqrr 4 0 2
        if ip == 28:
            yield r[4]

        ip = r[ipr] + 1

        if ip not in lines:
            return 'halt'


@aoc.test({})
def part_1(data: aoc.Data):
    return next(run_program(data))


@aoc.test({})
def part_2(data: aoc.Data):
    seen = set()
    last = None
    for r4 in run_program(data, part=2):
        if r4 in seen:
            return last
        seen.add(r4)
        last = r4
