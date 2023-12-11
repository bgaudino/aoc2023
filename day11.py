from dataclasses import dataclass
from itertools import combinations


@dataclass
class Image:
    map: list[str]

    def empty_space(self) -> tuple[list[int], list[int]]:
        rows: list[int] = []
        columns: list[int] = []
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == '#':
                    rows.append(y)
                    columns.append(x)
        rows = [i for i in range(len(self.map)) if i not in rows]
        columns = [i for i in range(len(self.map[0])) if i not in columns]
        return rows, columns

    def galaxies(self) -> list[tuple[int, int]]:
        galaxies: list[tuple[int, int]] = list()
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == '#':
                    galaxies.append((x, y))
        return galaxies

    def expanded(self, rate: int) -> list[tuple[int, int]]:
        galaxies: list[tuple[int, int]] = list()
        rows, columns = self.empty_space()
        for x, y in self.galaxies():
            x += len([column for column in columns if column < x]) * rate
            y += len([row for row in rows if row < y]) * rate
            galaxies.append((x, y))
        return galaxies

    def total_distance(self, expansion_rate: int = 2) -> int:
        return sum(distance(a, b) for a, b in combinations(self.expanded(expansion_rate - 1), 2))


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def main():
    with open('data/day11.txt') as f:
        image = Image([line.strip() for line in f.readlines()])

    part1 = image.total_distance()
    assert part1 == 9734203
    print(f'Part 1: {part1}')

    part2 = image.total_distance(1_000_000)
    assert part2 == 568914596391
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main()
