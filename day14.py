NORTH, SOUTH, EAST, WEST = (0, -1), (0, 1), (1, 0), (-1, 0)


class Platform:
    def __init__(self, data: str) -> None:
        rounded_rocks: set[tuple[int, int]] = set()
        cubed_rocks: set[tuple[int, int]] = set()
        rows = data.split('\n')
        for y, line in enumerate(rows):
            for x, char in enumerate(line):
                if char == 'O':
                    rounded_rocks.add((x, y))
                elif char == '#':
                    cubed_rocks.add((x, y))
        self.rounded_rocks = rounded_rocks
        self.cubed_rocks = cubed_rocks
        self.height = len(rows)
        self.width = len(rows[0])

    def __str__(self) -> str:
        return self.state()

    def is_available(self, space: tuple[int, int]) -> bool:
        return all([
            0 <= space[0] < self.width, 0 <= space[1] < self.height,
            space not in self.rounded_rocks,
            space not in self.cubed_rocks,
        ])

    def tilt(self, direction: tuple[int, int]) -> None:
        while True:
            moved = False
            if direction in (NORTH, SOUTH):
                rng = range(1, self.height) if direction == NORTH else range(self.height - 1, -1, -1)
                for y in rng:
                    for x in range(self.width):
                        if self.move_if_possible((x, y), direction):
                            moved = True
            elif direction in (EAST, WEST):
                rng = range(1, self.width) if direction == WEST else range(self.width - 1, -1, -1)
                for x in rng:
                    for y in range(self.height):
                        if self.move_if_possible((x, y), direction):
                            moved = True
            if not moved:
                break

    def move_if_possible(self, rock: tuple[int, int], direction: tuple[int, int]) -> bool:
        if rock not in self.rounded_rocks:
            return False
        next_space = (rock[0] + direction[0], rock[1] + direction[1])
        if not self.is_available(next_space):
            return False
        self.rounded_rocks.remove(rock)
        self.rounded_rocks.add(next_space)
        return True

    def cycle(self, count: int = 1) -> None:
        for _ in range(count):
            for direction in (NORTH, WEST, SOUTH, EAST):
                self.tilt(direction)

    def find_loop(self) -> tuple[int, int]:
        i = 0
        states: dict[str, int] = {}
        while True:
            i += 1
            self.cycle()
            state = self.state()
            if state in states:
                offset = i
                cycle_length = i - states[state]
                return cycle_length, offset
            states[state] = i

    def load(self) -> int:
        return sum(self.height - y for _, y in self.rounded_rocks)

    def state(self) -> str:
        state = ''
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.rounded_rocks:
                    state += 'O'
                elif (x, y) in self.cubed_rocks:
                    state += '#'
                else:
                    state += '.'
            state += '\n'
        return state


def main():
    with open('data/day14.txt') as f:
        data = f.read()

    platform = Platform(data)
    platform.tilt(NORTH)
    part1 = platform.load()
    assert part1 == 103614
    print(f'Part 1: {part1}')

    platform = Platform(data)
    loop, offset = platform.find_loop()
    cycles = 1_000_000_000
    loops = (cycles - offset) // loop
    remaining = cycles - offset - loop * loops
    platform.cycle(remaining)
    part2 = platform.load()
    assert part2 == 83790
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main()
