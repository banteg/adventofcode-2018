from collections import defaultdict, Counter

import aoc


class WristDevice:
    opcodes = [
        'addi', 'addr',  # addition
        'muli', 'mulr',  # multiplication
        'bani', 'banr',  # bitwise and
        'bori', 'borr',  # bitwise or
        'seti', 'setr',  # assignment
        'grti', 'gtir', 'gtrr',  # greater than
        'eqir', 'eqri', 'eqrr',  # equality
    ]

    def test(self, before, code, after):
        '''find opcodes matching a sample'''
        found = []
        for opcode in self.opcodes:
            registers = before.copy()
            i, a, b, c = code
            getattr(self, opcode)(registers, a, b, c)
            if registers == after:
                found.append(opcode)
        return found

    def recover_opcodes(self, tests):
        '''recover opcode numbering'''
        subtests = defaultdict(list)
        for before, code, after in tests:
            subtests[code[0]].append((before, code, after))
        counts = defaultdict(Counter)
        for i in subtests:
            for test in subtests[i]:
                counts[i].update(self.test(*test))
        recovered = {}
        while len(recovered) < len(subtests):
            for i in counts:
                ok = [op for op in counts[i] if op not in recovered and counts[i][op] == len(subtests[i])]
                if len(ok) == 1:
                    recovered[ok[0]] = i
        return {i: op for op, i in recovered.items()}

    def run_program(self, program, opcodes):
        '''run a program using recovered opcodes'''
        registers = [0, 0, 0, 0]
        for i, a, b, c in program:
            getattr(self, opcodes[i])(registers, a, b, c)
        return registers

    def addr(self, r, a, b, c):
        r[c] = r[a] + r[b]

    def addi(self, r, a, b, c):
        r[c] = r[a] + b

    def mulr(self, r, a, b, c):
        r[c] = r[a] * r[b]

    def muli(self, r, a, b, c):
        r[c] = r[a] * b

    def banr(self, r, a, b, c):
        r[c] = r[a] & r[b]

    def bani(self, r, a, b, c):
        r[c] = r[a] & b

    def borr(self, r, a, b, c):
        r[c] = r[a] | r[b]

    def bori(self, r, a, b, c):
        r[c] = r[a] | b

    def setr(self, r, a, b, c):
        r[c] = r[a]

    def seti(self, r, a, b, c):
        r[c] = a

    def gtir(self, r, a, b, c):
        r[c] = 1 if a > r[b] else 0

    def grti(self, r, a, b, c):
        r[c] = 1 if r[a] > b else 0

    def gtrr(self, r, a, b, c):
        r[c] = 1 if r[a] > r[b] else 0

    def eqir(self, r, a, b, c):
        r[c] = 1 if a == r[b] else 0

    def eqri(self, r, a, b, c):
        r[c] = 1 if r[a] == b else 0

    def eqrr(self, r, a, b, c):
        r[c] = 1 if r[a] == r[b] else 0


@aoc.test({})
def part_1(data: aoc.Data):
    first = data.split('\n\n\n\n')[0]
    tests = [aoc.Data(x).ints_lines for x in first.split('\n\n')]
    device = WristDevice()
    return sum(len(device.test(*test)) >= 3 for test in tests)


@aoc.test({})
def part_2(data: aoc.Data):
    first, second = data.split('\n\n\n\n')
    tests = [aoc.Data(x).ints_lines for x in first.split('\n\n')]
    program = aoc.Data(second).ints_lines
    device = WristDevice()
    opcodes = device.recover_opcodes(tests)
    registers = device.run_program(program, opcodes)
    return registers[0]
