import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Set


@dataclass
class Card:
    winners: Set[int]
    numbers: Set[int]

    def winning_numbers(self):
        return self.numbers.intersection(self.winners)

    def value(self):
        val = 0
        for i in range(len(self.winning_numbers())):
            if i == 0:
                val = 1
            else:
                val *= 2
        return val


def main():
    with open('data/day04.txt') as f:
        cards = [parse_card(line) for line in f]

    part1 = sum(card.value() for card in cards)
    assert part1 == 21821
    print(f'Part 1: {part1}')

    scratch_cards: defaultdict[int, int] = defaultdict(int)
    for i, card in enumerate(cards, 1):
        scratch_cards[i] += 1
        win_count = len(card.winning_numbers())
        for j in range(i + 1, i + 1 + win_count):
            scratch_cards[j] += scratch_cards[i]

    part2 = sum(scratch_cards.values())
    assert part2 == 5539496
    print(f'Part 2: {part2}')


def parse_card(line: str) -> Card:
    winners, numbers = line.split(': ')[-1].split(' | ')
    winners = set(int(n) for n in re.split(r'\s+', winners) if n)
    numbers = set(int(n) for n in re.split(r'\s+', numbers) if n)
    return Card(winners, numbers)


if __name__ == '__main__':
    main()
