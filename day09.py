import re


def main():
    report: list[list[list[int]]] = []
    with open('data/day09.txt') as f:
        for line in f:
            report.append([[int(n) for n in re.split(r'\s+', line) if n]])

    part1, part2 = 0, 0
    for history in report:
        values = history[0]
        while not all_zero(values):
            values = get_differences(values)
            history.append(values)
        part1 += get_next_value(history)
        part2 += get_next_value(history, backwards=True)

    assert part1 == 1647269739
    print(f'Part 1: {part1}')
    assert part2 == 864
    print(f'Part 2: {part2}')


def get_differences(values: list[int]) -> list[int]:
    return [x - y for x, y in zip(values[1:], values[:-1])]


def all_zero(values: list[int]) -> bool:
    return all(v == 0 for v in values)


def get_next_value(sequences: list[list[int]], backwards: bool = False) -> int:
    s = sequences.copy()
    s[-1].insert(0, 0 if backwards else -1)
    for x, y in reversed(list(zip(s[1:], s[:-1]))):
        if backwards:
            y.insert(0, y[0] - x[0])
        else:
            y.append(y[-1] + x[-1])
    return s[0][0 if backwards else -1]


if __name__ == '__main__':
    main()
