from dataclasses import dataclass
from itertools import combinations


@dataclass
class Image:
    map: list[str]

    def expand(self):
        rows: set[int] = set()
        columns: set[int] = set()
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == '#':
                    rows.add(y)
                    columns.add(x)

        empty_rows = {i for i in range(len(self.map)) if i not in rows}
        empty_columns = {i for i in range(
            len(self.map[0])) if i not in columns}
        offset = 0
        for i in sorted(empty_rows):
            self.map.insert(i + offset, '.' * len(self.map[0]))
            offset += 1
        offset = 0
        for i in sorted(empty_columns):
            for y, row in enumerate(self.map):
                self.map[y] = f'{row[:i + offset]}.{row[i + offset:]}'
            offset += 1

    def galaxies(self) -> set[tuple[int, int]]:
        galaxies: set[tuple[int, int]] = set()
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == '#':
                    galaxies.add((x, y))
        return galaxies


with open('data/day11.txt') as f:
    data = [line.strip() for line in f.readlines()]


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


image = Image(data)
image.expand()
part1 = sum(distance(a, b) for a, b in combinations(image.galaxies(), 2))
print(part1)
