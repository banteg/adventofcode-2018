from collections import defaultdict
from dataclasses import dataclass
from itertools import count
from string import ascii_uppercase

import aoc

example = '''
    Step C must be finished before step A can begin.
    Step C must be finished before step F can begin.
    Step A must be finished before step B can begin.
    Step A must be finished before step D can begin.
    Step B must be finished before step E can begin.
    Step D must be finished before step E can begin.
    Step F must be finished before step E can begin.
    '''


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


@dataclass
class Worker:
    task: str = None
    remaining: int = None


@aoc.test({example: 15})
def part_2(data: aoc.Data):
    is_example = data == aoc.cleandoc(example)
    per_task = 1 if is_example else 61
    worker_num = 2 if is_example else 5

    remaining, reqs = parse_steps(data)
    weights = {s: per_task + ascii_uppercase.index(s) for s in remaining}
    workers = [Worker() for _ in range(worker_num)]
    finished = ''

    for t in count():
        for worker in workers:
            if worker.task:
                worker.remaining -= 1
                if worker.remaining == 0:
                    finished += worker.task
                    remaining.remove(worker.task)
                    worker.task = None
        for worker in workers:
            if not worker.task:
                busy = {worker.task for worker in workers}
                can_do = sorted(s for s in remaining if reqs[s] <= set(finished) and s not in busy)
                if can_do:
                    task = can_do[0]
                    worker.task = task
                    worker.remaining = weights[task]

        # print(f'{t}'.rjust(5), *[(worker.task or '.').center(5) for worker in workers], finished, sep='  ')
        if not remaining:
            return t
