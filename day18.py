from dataclasses import dataclass


DIRECTIONS = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1)}


@dataclass
class Dig:
    direction: tuple[int, int]
    distance: int
    color: str


digs: list[Dig] = []
with open('data/day18.txt') as f:
    for line in f:
        direction, distance, color = line.strip().split(' ')
        digs.append(
            Dig(DIRECTIONS[direction], int(distance), color[1:-1]))

trenches: set[tuple[int, int]] = set()
position = (0, 0)

for trench in digs:
    for _ in range(trench.distance):
        position = (position[0] + trench.direction[0],
                    position[1] + trench.direction[1])
        trenches.add(position)

min_x = min(x for x, _ in trenches)
max_x = max(x for x, _ in trenches) + 1
min_y = min(y for _, y in trenches)
max_y = max(y for _, y in trenches) + 1


def print_lagoon():
    lagoon: list[str] = []
    for y in range(min_y, max_y):
        row = ''
        for x in range(min_x, max_x):
            if (x, y) in trenches:
                row += '*'
            else:
                row += '.'
        lagoon.append(row)
    print('\n'.join(lagoon))
    print()


queue: list[tuple[int, int]] = [(1, 1)]
filled: set[tuple[int, int]] = set()
seen: set[tuple[int, int]] = set()
while queue:
    x, y = queue.pop(0)
    if (x, y) in trenches:
        continue
    trenches.add((x, y))
    for n in ((
        (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)
    )):
        if n not in trenches and min_x <= n[0] <= max_x and min_y <= n[1] <= max_y:
            queue.append(n)
print(len(trenches))
