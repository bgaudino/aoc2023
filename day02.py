from collections import defaultdict
from math import prod

BAG = {'red': 12, 'green': 13, 'blue': 14}


def main():
    possible_games = []
    powers = []
    with open('data/day02.txt') as f:
        for line in f.readlines():
            game_id, ball_counts = parse(line)
            if is_possible(ball_counts):
                possible_games.append(game_id)
            powers.append(prod(ball_counts.values()))

    print(f'Part 1: {sum(possible_games)}')
    print(f'Part 2: {sum(powers)}')


def parse(line):
    game, balls = line.split(': ')
    game_id = int(game.split(' ')[-1])
    subsets = balls.split('; ')
    ball_counts = defaultdict(int)
    for subset in subsets:
        for ball in subset.split(', '):
            count, color = ball.strip().split(' ')
            ball_counts[color] = max(int(count), ball_counts[color])
    return game_id, ball_counts


def is_possible(ball_count):
    for color, count in BAG.items():
        if count < ball_count.get(color, 0):
            return False
    return True


if __name__ == '__main__':
    main()
