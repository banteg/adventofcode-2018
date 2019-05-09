from itertools import combinations

import networkx as nx

import aoc


examples = {
    '''
    0,0,0,0
    3,0,0,0
    0,3,0,0
    0,0,3,0
    0,0,0,3
    0,0,0,6
    9,0,0,0
    12,0,0,0
    ''': 2,
    '''
    -1,2,2,0
    0,0,2,-2
    0,0,0,-2
    -1,2,0,0
    -2,-2,-2,2
    3,0,2,-1
    -1,3,2,2
    -1,0,-1,0
    0,2,1,-2
    3,0,0,0
    ''': 4,
    '''
    1,-1,0,1
    2,0,-1,0
    3,2,-1,0
    0,0,3,1
    0,0,-1,-1
    2,3,-2,0
    -2,2,0,0
    2,-2,0,-1
    1,-1,0,-1
    3,2,0,2
    ''': 3,
    '''
    1,-1,-1,-2
    -2,-2,0,1
    0,2,1,3
    -2,3,-2,1
    0,2,3,-2
    -1,-1,1,-2
    0,-2,-1,0
    -2,2,3,-1
    1,2,2,0
    -1,-2,0,-2
    ''': 8,
}


def manhattan_distance(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


def find_constellations(points):
    G = nx.Graph()
    G.add_nodes_from(points)
    G.add_edges_from(
        (a, b) for a, b in combinations(points, 2) if manhattan_distance(a, b) <= 3
    )
    return nx.number_connected_components(G)


@aoc.test(examples)
def part_1(data: aoc.Data):
    points = [tuple(coords) for coords in data.ints_lines]
    return find_constellations(points)
