from collections import defaultdict
from math import prod

BAG = {'red': 12, 'green': 13, 'blue': 14}


def main():
    possible_games = []
    powers = []
    with open('data/day02.txt') as f:
        for line in f:
            game_id, ball_counts = parse(line)
            if is_possible(ball_counts):
                possible_games.append(game_id)
            powers.append(prod(ball_counts.values()))

    part1 = sum(possible_games)
    assert part1 == 2716
    print(f'Part 1: {part1}')

    part2 = sum(powers)
    assert part2 == 72227
    print(f'Part 2: {part2}')


def parse(line: str) -> tuple[int, defaultdict[str, int]]:
    game, balls = line.split(': ')
    game_id = int(game.split(' ')[-1])
    subsets = balls.split('; ')
    ball_counts: defaultdict[str, int] = defaultdict(int)
    for subset in subsets:
        for ball in subset.split(', '):
            count, color = ball.strip().split(' ')
            ball_counts[color] = max(int(count), ball_counts[color])
    return game_id, ball_counts


def is_possible(ball_count: defaultdict[str, int]) -> bool:
    for color, count in BAG.items():
        if count < ball_count.get(color, 0):
            return False
    return True


if __name__ == '__main__':
    main()
