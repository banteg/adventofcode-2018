from collections import Counter
from itertools import combinations
import adventofcode

data = adventofcode.load_input(2).splitlines()
# data = 'abcdef,bababc,abbcde,abcccd,aabcdd,abcdee,ababab'.split(',')

counts = Counter()

for line in data:
    line_counts = Counter()
    for a, v in Counter(line).items():
        line_counts[v] = 1
    counts += line_counts

print(counts[2] * counts[3])

# -- part 2 --

# data = '''abcde
# fghij
# klmno
# pqrst
# fguij
# axcye
# wvxyz'''.splitlines()

for p in combinations(data, 2):
    matching = [x for x, y in zip(*p) if x == y]
    distance = len(p[0]) - len(matching)
    if distance == 1:
        print(''.join(matching))
