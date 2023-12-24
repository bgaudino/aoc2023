from collections import deque

DIRECTIONS = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}


def main():
    with open('data/day23.txt') as f:
        trails = f.read().split('\n')
    part1 = longest_hike(trails)
    assert part1 == 2034
    print(f'Part 1: {part1}')


def longest_hike(trails: list[str]) -> int:
    max_steps = -1
    height, width = len(trails), len(trails[0])
    start = (trails[0].index('.'), 1)
    end = (trails[height - 1].index('.'), height - 2)
    dq: deque[tuple[int, tuple[int, int], set[tuple[int, int]]]] = deque()
    dq.append((2, start, set()))
    while dq:
        steps, position, seen = dq.pop()
        if position == end:
            max_steps = max(steps, max_steps)
            continue
        seen.add(position)
        x, y = position
        space = trails[y][x]
        if space in DIRECTIONS:
            directions = [DIRECTIONS[space]]
        else:
            directions = DIRECTIONS.values()
        for xx, yy in directions:
            new_position = (x + xx, y + yy)
            xxx, yyy = new_position
            if new_position in seen:
                continue
            if not (0 <= xxx < width and 0 < yyy < height):
                continue
            if trails[yyy][xxx] == '#':
                continue
            dq.append((steps + 1, new_position, seen.copy()))
    return max_steps


if __name__ == '__main__':
    main()
