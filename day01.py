from itertools import cycle
import adventofcode

data = [
    int(x) for x in
    adventofcode.load_input(1).splitlines()
]

value = 0
for adj in data:
    value += adj
print(value)

value = 0
seen = set()
for adj in cycle(data):
    value += adj
    if value in seen:
        break
    seen.add(value)

print(value)
