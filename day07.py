import aoc
from collections import defaultdict
from itertools import count


example = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''



def parse_steps(data):
    steps = set()
    reqs = defaultdict(set)
    for x in data.splitlines():
        req = x.split()[1]
        step = x.split()[7]
        reqs[step].add(req)
        steps.update({req, step})
    return steps, reqs


@aoc.test({example: 'CABDFE'})
def part_1(data: aoc.Data):
    steps, reqs = parse_steps(data)
    finished = ''
    while len(finished) != len(steps):
        available = set()
        for step in steps - set(finished):
            if reqs[step] <= set(finished):
                available.add(step)
        finished += sorted(available)[0]
    return finished
