import re

NUMBERS = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def main():
    with open('data/day01.txt') as f:
        document = f.readlines()

    part1 = sum(get_calibration_value(line) for line in document)
    assert part1 == 54331
    print(f'Part 1: {part1}')

    pattern = fr"(?=(\d|{'|'.join(NUMBERS)}))"
    part2 = sum(get_calibration_value(line, pattern) for line in document)
    assert part2 == 54518
    print(f'Part 2: {part2}')


def get_calibration_value(text: str, pattern: str = r'\d') -> int:
    matches: list[str] = re.findall(pattern, text)
    return int(''.join(m if m.isdigit() else NUMBERS[m] for m in (matches[0], matches[-1])))


if __name__ == '__main__':
    main()
