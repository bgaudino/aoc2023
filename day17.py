import math
import heapq
from typing import NamedTuple


with open('data/day17.txt') as f:
    CITY = [[int(n) for n in row.strip()] for row in f]

MAX_X = len(CITY[0])
MAX_Y = len(CITY)


class Position(NamedTuple):
    x: int
    y: int


class Step(NamedTuple):
    position: Position
    direction: int
    moves: int


DIRECTIONS = (Position(-1, 0), Position(0, 1), Position(1, 0), Position(0, -1))
GOAL = Position(MAX_X - 1, MAX_Y - 1)


def move(p1: Position, p2: Position) -> Position:
    return Position(p1.x + p2.x, p1.y + p2.y)


def in_bounds(p: Position):
    return 0 <= p.x < MAX_X and 0 <= p.y < MAX_Y


def minimum_heat_loss(ultra_crucibles: bool = False):
    queue: list[tuple[int, Step]] = [(0, Step(Position(0, 0), -1, -1))]
    seen: set[Step] = set()
    min_heat_loss = math.inf
    while queue:
        heat_loss, step = heapq.heappop(queue)
        if step in seen:
            continue
        if step.position == GOAL:
            min_heat_loss = min(min_heat_loss, heat_loss)
            continue
        seen.add(step)

        for new_direction, delta in enumerate(DIRECTIONS):
            if (new_direction + 2) % 4 == step.direction:
                continue
            new_moves = step.moves + 1 if new_direction == step.direction else 1
            if ultra_crucibles:
                if new_moves > 10:
                    continue
                if 0 < step.moves < 4 and new_direction != step.direction:
                    continue
            elif new_direction == step.direction:
                if new_moves > 3:
                    continue
            new_position = move(step.position, delta)
            if not in_bounds(new_position):
                continue

            new_heat_loss = heat_loss + CITY[new_position.y][new_position.x]
            next_step = Step(new_position, new_direction, new_moves)
            if next_step in seen:
                continue
            heapq.heappush(queue, (new_heat_loss, next_step))

    return min_heat_loss


def main():
    part1 = minimum_heat_loss()
    print(part1)
    assert part1 == 953
    part2 = minimum_heat_loss(ultra_crucibles=True)
    print(part2)
    assert part2 == 1180


if __name__ == '__main__':
    main()
