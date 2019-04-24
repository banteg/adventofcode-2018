from collections import defaultdict, Counter

import aoc


def addr(r, a, b): return r[a] + r[b]
def addi(r, a, b): return r[a] + b

def mulr(r, a, b): return r[a] * r[b]
def muli(r, a, b): return r[a] * b

def banr(r, a, b): return r[a] & r[b]
def bani(r, a, b): return r[a] & b

def borr(r, a, b): return r[a] | r[b]
def bori(r, a, b): return r[a] | b

def setr(r, a, b): return r[a]
def seti(r, a, b): return a

def gtir(r, a, b): return 1 if a > r[b] else 0
def grti(r, a, b): return 1 if r[a] > b else 0
def gtrr(r, a, b): return 1 if r[a] > r[b] else 0

def eqir(r, a, b): return 1 if a == r[b] else 0
def eqri(r, a, b): return 1 if r[a] == b else 0
def eqrr(r, a, b): return 1 if r[a] == r[b] else 0


opcodes = [
    addr, addi,
    mulr, muli,
    banr, bani,
    borr, bori,
    setr, seti,
    gtir, grti, gtrr,
    eqir, eqri, eqrr,
]


def looks_like(before, code, after):
    '''find opcodes matching a sample'''
    found = []
    for opcode in opcodes:
        r = before.copy()
        i, a, b, c = code
        r[c] = opcode(r, a, b)
        if r == after:
            found.append(opcode)
    return found


def recover_opcodes(tests):
    '''recover opcode numbering'''
    subtests = defaultdict(list)
    for before, code, after in tests:
        subtests[code[0]].append((before, code, after))
    counts = defaultdict(Counter)
    for i in subtests:
        for test in subtests[i]:
            counts[i].update(looks_like(*test))
    recovered = {}
    while len(recovered) < len(subtests):
        for i in counts:
            ok = [op for op in counts[i] if op not in recovered and counts[i][op] == len(subtests[i])]
            if len(ok) == 1:
                recovered[ok[0]] = i
    return {i: op for op, i in recovered.items()}


def run_program(program, codes):
    '''run a program using recovered opcodes'''
    r = [0, 0, 0, 0]
    for i, a, b, c in program:
        r[c] = codes[i](r, a, b)
    return r


@aoc.test({})
def part_1(data: aoc.Data):
    first = data.split('\n\n\n\n')[0]
    tests = [aoc.Data(x).ints_lines for x in first.split('\n\n')]
    return sum(len(looks_like(*test)) >= 3 for test in tests)


@aoc.test({})
def part_2(data: aoc.Data):
    first, second = data.split('\n\n\n\n')
    tests = [aoc.Data(x).ints_lines for x in first.split('\n\n')]
    program = aoc.Data(second).ints_lines
    opcodes = recover_opcodes(tests)
    registers = run_program(program, opcodes)
    return registers[0]
