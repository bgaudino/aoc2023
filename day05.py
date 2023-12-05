import re
from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class MapItem:
    start: int
    end: int
    difference: int

    def __lt__(self, other) -> bool:
        return self.start < other.start

    def contains(self, n: int) -> bool:
        return self.start <= n < self.end

    def convert(self, n: int) -> int:
        return n + self.difference


class Map:
    __slots__ = ['items']

    def __init__(self, items: list[MapItem]):
        self.items = sorted(items)

    def convert(self, n: int) -> int:
        if item := self.search(n):
            return item.convert(n)
        return n

    def search(self, n: int) -> Optional[MapItem]:
        low, high = 0, len(self.items) - 1
        while low <= high:
            middle = low + (high - low) // 2
            item = self.items[middle]
            if item.contains(n):
                return item
            elif n >= item.end:
                low = middle + 1
            else:
                high = middle - 1
        return None

    def seeds_from_range(self, start: int, length: int) -> list[int]:
        return list(i for i in range(start, start + length))


@dataclass
class Almanac:
    maps: list[Map]

    def location(self, seed: int) -> int:
        for m in self.maps:
            seed = m.convert(seed)
        return seed

    def closest_location(self, seeds: list[int]) -> int:
        return min(self.location(seed) for seed in seeds)


def parse() -> tuple[list[int], Almanac]:
    with open('data/day05.txt') as f:
        a, *b = f.read().split('\n\n')
    seeds = [int(n) for n in re.split(r'\s+', a)[1:]]
    maps = []
    for m in b:
        items = []
        for line in m.split('\n')[1:]:
            dst, src, rng = map(int, re.split(r'\s+', line))
            items.append(MapItem(src, src + rng, dst - src))
        maps.append(Map(items))
    return seeds, Almanac(maps)


def main():
    seeds, almanac = parse()

    part1 = almanac.closest_location(seeds)
    assert part1 == 178159714
    print(f'Part 1: {part1}')

    pairs = []
    for i in range(0, len(seeds), 2):
        pairs.append(seeds[i:i + 2])
    seeds = []
    for i, pair in enumerate(pairs):
        seeds += almanac.maps[0].seeds_from_range(*pair)

    # TODO: make not slow as shit
    part2 = almanac.closest_location(seeds)
    assert part2 == 100165128
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main()
