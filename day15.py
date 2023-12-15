import re
from collections import defaultdict


class Lens(str):
    def __init__(self, s: str) -> None:
        super().__init__()
        self.label, self.operation, length = (re.split(r'([=-])', s))
        self.length = int(length or 0)


def HASH(s: str) -> int:
    value = 0
    for ch in s:
        value += ord(ch)
        value *= 17
        value = value % 256
    return value


def focusing_power(HASHMAP: dict[int, list[Lens]]) -> int:
    power = 0
    for box, lenses in HASHMAP.items():
        for i, lens in enumerate(lenses):
            power += (box + 1) * (i + 1) * lens.length
    return power


def main():
    with open('data/day15.txt') as f:
        lenses = [Lens(s) for s in f.read().split(',')]

    part1 = sum(HASH(lens) for lens in lenses)
    assert part1 == 498538
    print(f'Part 1: {part1}')

    HASHMAP: dict[int, list[Lens]] = defaultdict(list)
    for lens in lenses:
        h = HASH(lens.label)
        if lens.operation == '-':
            for i, l in enumerate(HASHMAP[h]):
                if l.label == lens.label:
                    HASHMAP[h].pop(i)
                    break
        elif lens.operation == '=':
            for i, l in enumerate(HASHMAP[h]):
                if l.label == lens.label:
                    HASHMAP[h][i] = lens
                    break
            else:
                HASHMAP[h].append(lens)
    part2 = focusing_power(HASHMAP)
    assert part2 == 286278
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main()
