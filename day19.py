import aoc


examples = {
    '''#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5''': 6
}

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


def run_program(code):
    r = [0, 0, 0, 0, 0, 0]
    ipr, *program = code.splitlines()
    ipr = int(ipr.split()[1])
    lines = dict(enumerate(program))

    ip = 0
    while True:
        i, *args = lines[ip].split()
        a, b, c = [int(x) for x in args]
        r[ipr] = ip
        bef = r.copy()
        r[c] = codes[i](r, a, b)
        ip = r[ipr] + 1
        # print(f'{n} ip={ip} {bef} {lines[ip]} {r}')
        if ip not in lines:
            return r[0]


def run_optimized(code, r0):
    r = [r0, 0, 0, 0, 0, 0]
    ipr, *program = code.splitlines()
    ipr = int(ipr.split()[1])
    lines = dict(enumerate(program))

    ip = 0
    while True:
        i, *args = lines[ip].split()
        a, b, c = [int(x) for x in args]
        r[ipr] = ip
        if ip == 1:
            divisors = [x for x in range(1, r[5] + 1) if not r[5] % x]
            return sum(divisors)
        else:
            r[c] = codes[i](r, a, b)
        ip = r[ipr] + 1
        if ip not in lines:
            return r[0]


@aoc.test(examples)
def part_1(data: aoc.Data):
    return run_program(data)


@aoc.test({})
def part_2(data: aoc.Data):
    return run_optimized(data, 1)
