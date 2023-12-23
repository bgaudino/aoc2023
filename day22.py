from typing import NamedTuple


class Cube(NamedTuple):
    x: int
    y: int
    z: int


def main():
    bricks = parse_bricks()
    container = set(cube for brick in bricks for cube in brick)
    bricks, *_ = fall(bricks, container)
    part1, part2 = 0, 0
    for brick in bricks:
        supporting = num_supporting(brick, bricks, container)
        if supporting:
            part2 += supporting
        else:
            part1 += 1
    assert part1 == 437
    print(f'Part 1: {part1}')
    assert part2 == 42561
    print(f'Part 2: {part2}')


def parse_bricks() -> list[set[Cube]]:
    bricks: list[set[Cube]] = []
    with open('data/day22.txt') as f:
        for line in f:
            a, b = line.strip().split('~')
            x_start, y_start, z_start = [int(n) for n in a.split(',')]
            x_stop, y_stop, z_stop = [int(n) for n in b.split(',')]
            brick: set[Cube] = set()
            for x in range(x_start, x_stop + 1):
                for y in range(y_start, y_stop + 1):
                    for z in range(z_start, z_stop + 1):
                        brick.add(Cube(x, y, z))
            bricks.append(brick)
    return bricks


def fall(bricks: list[set[Cube]], container: set[Cube]) -> tuple[list[set[Cube]], set[int]]:
    bricks.sort(key=lambda x: max(c.z for c in x))
    moving = True
    bricks_fell: set[int] = set()
    while moving:
        new_bricks: list[set[Cube]] = []
        moving = False
        for i, brick in enumerate(bricks):
            new_brick, brick_moved = _fall(brick, container)
            if brick_moved:
                moving = True
                bricks_fell.add(i)
            new_bricks.append(new_brick)
        bricks = new_bricks
    return bricks, bricks_fell


def _fall(brick: set[Cube], container: set[Cube]) -> tuple[set[Cube], bool]:
    container.difference_update(brick)
    moved = False
    while True:
        next_location = set(Cube(c.x, c.y, c.z - 1) for c in brick)
        if next_location.intersection(container):
            break
        on_floor = False
        for c in next_location:
            if c.z <= 0:
                on_floor = True
                break
        if on_floor:
            break
        brick = next_location
        moved = True
    container.update(brick)
    return brick, moved


def num_supporting(brick: set[Cube], bricks: list[set[Cube]], container: set[Cube]) -> int:
    c = container.copy()
    c.difference_update(brick)
    bl = [b for b in bricks if b != brick]
    _, bricks_fell = fall(bl, c)
    return len(bricks_fell)


if __name__ == '__main__':
    main()
