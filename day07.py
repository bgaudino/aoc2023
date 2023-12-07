from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import Self, Iterable

CARD_RANKS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}


class HandType(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@dataclass
class Hand:
    cards: str
    bid: int
    jokers: bool = False

    def __lt__(self, other: Self) -> bool:
        x, y = self.type(), other.type()
        if x == y:
            return self.card_values() < other.card_values()
        return x.value < y.value

    def counter(self) -> Counter[str]:
        counter = Counter(self.cards)
        if self.jokers and 'J' in counter and 0 < counter['J'] < 5:
            jokers = counter.pop('J', 0)
            most_common = counter.most_common(1)[0][0]
            counter[most_common] += jokers
        return counter

    def card_values(self) -> list[int]:
        return [
            1 if self.jokers and card == 'J'
            else CARD_RANKS[card] for card in self.cards
        ]

    def type(self) -> HandType:
        counter = self.counter()
        unique_cards = len(counter)
        if unique_cards == 1:
            return HandType.FIVE_OF_A_KIND
        if unique_cards == 2:
            for count in counter.values():
                if count in (1, 4):
                    return HandType.FOUR_OF_A_KIND
                return HandType.FULL_HOUSE
        if unique_cards == 3:
            for count in counter.values():
                if count == 3:
                    return HandType.THREE_OF_A_KIND
            return HandType.TWO_PAIR
        if unique_cards == 4:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD


def calculate_winnings(hands: Iterable[Hand]) -> int:
    return sum(hand.bid * i for i, hand in enumerate(sorted(hands), 1))


def main():
    with open('data/day07.txt') as f:
        hands: list[Hand] = []
        for line in f:
            cards, bid, = line.strip().split(' ')
            hands.append(Hand(cards, int(bid)))

    part1 = calculate_winnings(hands)
    assert part1 == 247815719
    print(f'Part 1: {part1}')

    for hand in hands:
        hand.jokers = True
    part2 = calculate_winnings(hands)
    assert part2 == 248747492
    print(f'Part 2: {part2}')


if __name__ == '__main__':
    main()
