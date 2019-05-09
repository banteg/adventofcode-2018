from collections import defaultdict
from dataclasses import dataclass
from itertools import count
from string import ascii_uppercase

import networkx as nx

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
    id_: int
    task: str = None
    remaining: int = None

    def __repr__(self):
        status = f'{self.task} {self.remaining}s' if self.task else '...'
        return f'<W{self.id_}: {status}>'


@aoc.test({example: 15})
def part_2(data: aoc.Data):
    is_example = data == aoc.cleandoc(example)
    per_task = 1 if is_example else 61
    worker_num = 2 if is_example else 5

    G = nx.DiGraph()
    for x in data.splitlines():
        req = x.split()[1]
        step = x.split()[7]
        G.add_node(step, weight=per_task + ascii_uppercase.index(step))
        G.add_node(req, weight=per_task + ascii_uppercase.index(req))
        G.add_edge(step, req)

    completed = ''
    workers = [Worker(n) for n in range(worker_num)]
    for t in count():
        for worker in workers:
            if worker.task:
                worker.remaining -= 1
                if worker.remaining == 0:
                    completed += worker.task
                    G.remove_node(worker.task)
                    worker.task = None
        for worker in workers:
            if not worker.task:
                busy = {worker.task for worker in workers}
                can_do = sorted(n for n, d in G.out_degree if d == 0 and n not in busy)
                if can_do:
                    task = can_do[0]
                    worker.task = task
                    worker.remaining = G.nodes[task]['weight']

        # print(f'{t}'.rjust(5), *[(worker.task or '.').center(5) for worker in workers], completed, sep='  ')
        if not G:
            return t
