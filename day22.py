from typing import NamedTuple


class Cube(NamedTuple):
    x: int
    y: int
    z: int


def main():
    blocks = parse_blocks()
    container = set(cube for block in blocks for cube in block)
    blocks, _ = fall(blocks, container)
    part1 = len([b for b in blocks if can_disintegrate(b, blocks, container)])
    assert part1 == 437
    print(f'Part 1: {part1}')


def parse_blocks() -> list[set[Cube]]:
    blocks: list[set[Cube]] = []
    with open('data/day22.txt') as f:
        for line in f:
            a, b = line.strip().split('~')
            x_start, y_start, z_start = [int(n) for n in a.split(',')]
            x_stop, y_stop, z_stop = [int(n) for n in b.split(',')]
            block: set[Cube] = set()
            for x in range(x_start, x_stop + 1):
                for y in range(y_start, y_stop + 1):
                    for z in range(z_start, z_stop + 1):
                        block.add(Cube(x, y, z))
            blocks.append(block)
    return blocks


def fall(blocks: list[set[Cube]], container: set[Cube]) -> tuple[list[set[Cube]], bool]:
    blocks.sort(key=lambda x: max(c.z for c in x))
    moved = False
    moving = True
    while moving:
        new_blocks: list[set[Cube]] = []
        moving = False
        for block in blocks:
            new_block, block_moved = _fall(block, container)
            if block_moved:
                moving = True
                moved = True
            new_blocks.append(new_block)
        blocks = new_blocks
    return blocks, moved


def _fall(block: set[Cube], container: set[Cube]) -> tuple[set[Cube], bool]:
    container.difference_update(block)
    moved = False
    while True:
        next_location = set(Cube(c.x, c.y, c.z - 1) for c in block)
        if next_location.intersection(container):
            break
        on_floor = False
        for c in next_location:
            if c.z <= 0:
                on_floor = True
                break
        if on_floor:
            break
        block = next_location
        moved = True
    container.update(block)
    return block, moved


def can_disintegrate(block: set[Cube], blocks: list[set[Cube]], container: set[Cube]):
    c = container.copy()
    c.difference_update(block)
    bl = [b for b in blocks if b != block]
    _, moved = fall(bl, c)
    return not moved


if __name__ == '__main__':
    main()
