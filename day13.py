
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass
class Pattern:
    pattern: list[str]

    def rocks(self) -> tuple[dict[int, set[int]], dict[int, set[int]]]:
        rows: dict[int, set[int]] = defaultdict(set)
        columns: dict[int, set[int]] = defaultdict(set)
        for y, line in enumerate(self.pattern):
            for x, char in enumerate(line):
                if char == '#':
                    rows[y].add(x)
                    columns[x].add(y)
        return rows, columns

    def summary(self, allowed_differences: int = 0) -> int:
        rows, columns = self.rocks()
        row = self.find_reflection(rows, allowed_differences)
        if row is not None:
            return (row + 1) * 100
        column = self.find_reflection(columns, allowed_differences)
        if column is not None:
            return column + 1
        return 0

    def find_reflection(self, rocks: dict[int, set[int]], allowed_differences: int) -> Optional[int]:
        size = len(rocks)
        for i in range(size - 1):
            j, k = i, i + 1
            differences = 0
            while j >= 0 and k < size:
                differences += len(rocks[j].symmetric_difference(rocks[k]))
                if differences > allowed_differences:
                    break
                j -= 1
                k += 1
            else:
                if differences == allowed_differences:
                    return i
        return None


def main():
    with open('data/day13.txt') as f:
        patterns = [Pattern(p.split('\n')) for p in f.read().split('\n\n')]

    part1 = sum(p.summary() for p in patterns)
    assert part1 == 35210
    print(f'Part 1: {part1}')
    part2 = sum(p.summary(1) for p in patterns)
    assert part2 == 31974
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main()
