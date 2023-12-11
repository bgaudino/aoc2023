from typing import TypeAlias

Coord: TypeAlias = tuple[int, int]

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

DIRECTIONS: dict[Coord, Coord] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST
}

PIPES = {
    '|': (NORTH, SOUTH),
    '-': (EAST, WEST),
    'L': (NORTH, EAST),
    'J': (NORTH, WEST),
    'F': (SOUTH, EAST),
    '7': (SOUTH, WEST),
}

pipes: dict[Coord, tuple[Coord, Coord]] = {}
start = None
with open('data/day10.txt') as f:
    maze = [line.strip() for line in f]

for y, line in enumerate(maze):
    for x, c in enumerate(line):
        if c == 'S':
            start = (x, y)
        pipe = PIPES.get(c)
        if pipe is not None:
            pipes[(x, y)] = pipe


def find_loop(start: Coord, pipes: dict[Coord, tuple[Coord, Coord]]) -> list[tuple[Coord, Coord]]:
    paths: list[list[tuple[Coord, Coord]]] = [[(start, d)] for d in DIRECTIONS]
    while paths:
        path = paths.pop(0)
        src, out_direction = path[-1]
        dst = move(src, out_direction)
        if dst == start:
            return path
        in_direction = DIRECTIONS[out_direction]
        if dst in pipes and in_direction in pipes[dst]:
            paths.extend([
                [*path, (dst, d)] for d in pipes[dst] if d != in_direction
            ])
    return []


def move(pipe: Coord, direction: Coord) -> Coord:
    return (pipe[0] + direction[0], pipe[1] + direction[1])


if start is None:
    exit()

loop = find_loop(start, pipes)
print(len(loop) // 2)

loop_pipes = {pipe for pipe, _ in loop}

inside_count = 0
for y, row in enumerate(maze):
    groups: list[list[Coord]] = []
    group: list[Coord] = []
    seperator: str = ''
    for x, char in enumerate(row):
        if (x, y) not in loop_pipes:
            group.append((x, y))
            seperator = ''
        elif char in ('F', 'L'):
            seperator = char
        elif char == '|' or (seperator == 'F' and char == 'J') or (seperator == 'L' and char == '7'):
            groups.append(group)
            group = []
            seperator = ''
        elif char == '-' and seperator in ('F', 'L'):
            continue
        else:
            seperator = ''
    count = sum(len(group) for i, group in enumerate(groups) if i % 2 != 0)
    inside_count += count
print(inside_count)