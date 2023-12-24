import re
from itertools import combinations
from typing import NamedTuple


class HailStone(NamedTuple):
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int


def main():
    stones: list[HailStone] = []
    with open('data/day24.txt') as f:
        for line in f:
            p, v = line.strip().split(' @ ')
            px, py, pz = [int(m) for m in re.findall(r'-?\d+', p)]
            vx, vy, vz = [int(m) for m in re.findall(r'-?\d+', v)]
            stones.append(HailStone(px, py, pz, vx, vy, vz))
    intersections = [(a, b) for a, b in combinations(
        stones, 2) if intersect_in_test_area(a, b)]
    print(f'Part 1: {len(intersections)}')


def calculate_intersection(a: HailStone, b: HailStone):
    if a.vx * b.vy - a.vy * b.vx == 0:
        return None
    t = ((b.px - a.px) * b.vy - (b.py - a.py) * b.vx) / (a.vx * b.vy - a.vy * b.vx)
    return (a.px + t * a.vx, a.py + t * a.vy)


def intersect_in_test_area(a: HailStone, b: HailStone):
    intersection = calculate_intersection(a, b)
    if intersection is None:
        return False
    if not all(200000000000000 <= p <= 400000000000000 for p in (intersection)):
        return False
    if any(in_past(h, intersection) for h in (a, b)):
        return False
    return True


def in_past(a: HailStone, b: tuple[float, float]):
    x, y = b
    xx, yy = a.px + a.vx, a.py + a.vy
    return abs(xx - x) + abs(yy - y) > abs(a.px - x) + abs(a.py - y)


if __name__ == '__main__':
    main()
