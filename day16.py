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
        found = []
        for opcode in self.opcodes:
            registers = before.copy()
            i, a, b, c = code
            getattr(self, opcode)(registers, a, b, c)
            if registers == after:
                found.append(opcode)
        return found

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
    first = data.split('\n\n\n')[0]
    tests = [aoc.Data(x).ints_lines for x in first.split('\n\n')]
    vm = WristDevice()
    return sum(len(vm.test(*test)) >= 3 for test in tests)
