import re
from collections import defaultdict

with open('data/day03.txt') as f:
    schematic = f.readlines()

max_x, max_y = len(schematic[0]), len(schematic)


def main():
    parts = []
    gears = defaultdict(list)
    for y, line in enumerate(schematic):
        current_part = ''
        for x, char in enumerate(line):
            if char.isdigit():
                current_part += char
            elif current_part:
                part, gear = get_part(x, y, current_part)
                if part:
                    parts.append(int(current_part))
                if gear:
                    gears[gear].append(part)
                current_part = ''
    part1 = sum(parts)
    assert part1 == 539590
    print(f'Part 1: {part1}')

    ratios = [p[0] * p[1] for p in gears.values() if len(p) == 2]
    part2 = sum(ratios)
    assert part2 == 80703636
    print(f'Part 2: {part2}')


def get_part(x, y, part):
    neighbors = []
    if y - 1 >= 0:
        neighbors += [
            (i, y - 1) for i in range(max(0, x - len(part) - 1), x + 1)
        ]
    if x - len(part) - 1 >= 0:
        neighbors.append((x - len(part) - 1, y))
    neighbors.append((x, y))
    if y + 1 < max_y:
        neighbors += [
            (i, y + 1) for i in range(max(0, x - len(part) - 1), x + 1)
        ]
    for i, j in neighbors:
        char = schematic[j][i]
        if not re.match(r'\d|\.|\n', char):
            return int(part), (i, j) if char == '*' else None
    return None, None


if __name__ == '__main__':
    main()
