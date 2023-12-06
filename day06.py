import re
from dataclasses import dataclass
from math import prod


@dataclass
class Race:
    time: int
    record: int

    def ways_to_win(self) -> int:
        for speed in range(1, self.time):
            if (self.time - speed) * speed > self.record:
                return self.time + 1 - 2 * speed
        return 0


def main():
    with open('data/day06.txt') as f:
        data = f.readlines()

    times = map(int, re.findall(r'\d+', data[0]))
    records = map(int, re.findall(r'\d+', data[1]))
    races = (Race(t, r) for t, r in zip(times, records))
    part1 = prod(r.ways_to_win() for r in races)
    assert part1 == 440000
    print(part1)

    time = int(re.sub(r'\D', '', data[0]))
    record = int(re.sub(r'\D', '', data[1]))
    race = Race(time, record)
    part2 = race.ways_to_win()
    assert part2 == 26187338
    print(part2)


if __name__ == '__main__':
    main()
