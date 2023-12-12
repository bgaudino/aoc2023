import re
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Record:
    damaged: str
    groups: list[int]

    def total_springs(self) -> int:
        return sum(self.groups)

    def missing_springs(self) -> int:
        return self.total_springs() - self.damaged.count('#')

    def unknown(self) -> list[int]:
        return [i for i, char in enumerate(self.damaged) if char == '?']

    def pattern(self) -> str:
        regex = '\\.*'
        for i, n in enumerate(self.groups):
            regex += f'\\#{{{n}}}\\.'
            if i == len(self.groups) - 1:
                regex += '*'
            else:
                regex += '+'
        return regex

    def possible_arrangements(self) -> int:
        count = 0
        for combo in combinations(self.unknown(), self.missing_springs()):
            arrangement = ''
            for i, char in enumerate(self.damaged):
                if char == '?':
                    arrangement += '#' if i in combo else '.'
                else:
                    arrangement += char
            if re.match(self.pattern(), arrangement):
                count += 1
        return count


def parse(text: str) -> Record:
    damaged, _, rest = text.partition(' ')
    groups = [int(n) for n in re.findall(r'\d+', rest)]
    return Record(damaged, groups)


def main():
    with open('data/day12.txt') as f:
        records = [parse(line) for line in f]

    part1 = sum(record.possible_arrangements() for record in records)
    print(part1)


if __name__ == '__main__':
    main()
