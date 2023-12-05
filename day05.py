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

    def reverse_convert(self, n: int) -> int:
        for item in self.items:
            if item.contains(n - item.difference):
                return n - item.difference
        return n


@dataclass
class Almanac:
    maps: list[Map]

    def location(self, seed: int) -> int:
        for m in self.maps:
            seed = m.convert(seed)
        return seed

    def closest_location(self, seeds: list[int]) -> int:
        return min(self.location(seed) for seed in seeds)

    def seed(self, location: int) -> int:
        for m in reversed(self.maps):
            location = m.reverse_convert(location)
        return location

    def seed_ranges(self, seeds: list[int]) -> list[list[int]]:
        return [seeds[i:i + 2] for i in range(0, len(seeds), 2)]

    def is_possible(self, location: int, seed_ranges: list[list[int]]) -> bool:
        seed = self.seed(location)
        for start, length in seed_ranges:
            if start <= seed < start + length:
                return True
        return False


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

    seed_ranges = almanac.seed_ranges(seeds)
    location = 0
    while True:
        if almanac.is_possible(location, seed_ranges):
            break
        location += 1
    assert location == 100165128
    print(f'Part 2: {location}')


if __name__ == '__main__':
    main()
