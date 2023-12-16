from collections import defaultdict
from typing import Iterator, TypeAlias

Coord: TypeAlias = tuple[int, int]
DIRECTIONS = {
    '^': (0, -1), 'v': (0, 1), '>': (1, 0), '<': (-1, 0), '.': (0, 0)
}
MIRRORS: dict[str, dict[str, tuple[str, ...]]] = {
    '\\': {'^': ('<',), 'v': ('>',), '>': ('v',), '<': ('^',)},
    '/': {'^': ('>',), 'v': ('<',), '>': ('^',), '<': ('v',)},
    '-': {'^': ('<', '>'), 'v': ('<', '>'), '>': ('>',), '<': ('<',)},
    '|': {'^': ('^',), 'v': ('v',), '>': ('^', 'v'), '<': ('^', 'v')},
    '.': {'^': ('^',), 'v': ('v',), '>': ('>',), '<': ('<',)},
}

CONTRAPTION: dict[Coord, str] = {}
with open('data/day16.txt') as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            CONTRAPTION[(x, y)] = char

MAX_X = max(x for x, _ in CONTRAPTION)
MAX_Y = max(y for _, y in CONTRAPTION)


def in_bounds(location: tuple[int, int]) -> bool:
    return 0 <= location[0] <= MAX_X and 0 <= location[1] <= MAX_Y


def energize(start: Coord, direction: str):
    beams: list[list[tuple[Coord, str]]] = [[(start, direction)]]
    seen: dict[Coord, set[str]] = defaultdict(set)

    while beams:
        beam = beams.pop(0)
        location, direction = beam[-1]
        delta = DIRECTIONS[direction]
        if location != start and direction in seen[location]:
            continue
        if in_bounds(location):
            seen[location].add(direction)
        next_location = (location[0] + delta[0], location[1] + delta[1])
        if not in_bounds(next_location):
            continue
        next_space = CONTRAPTION[next_location]
        for d in MIRRORS[next_space][direction]:
            beams.append([*beam, (next_location, d)])
    return len(seen)


def starting_points() -> Iterator[tuple[Coord, str]]:
    for y in range(MAX_Y + 1):
        if y == 0:
            yield from (((x, -1), 'v') for x in range(MAX_X + 1))
        elif y == MAX_Y:
            yield from (((x, MAX_Y + 1), '^') for x in range(MAX_X + 1))
        else:
            yield ((-1, 0), '>')
            yield ((MAX_X + 1, 0), '<')


def main():
    energy = {start: energize(*start) for start in starting_points()}
    part1 = energy[((-1, 0), '>')]
    print(f'Part 1: {part1}')
    assert part1 == 7307
    part2 = max(energy.values())
    print(f'Part 2: {part2}')
    assert part2 == 7635


if __name__ == '__main__':
    main()
