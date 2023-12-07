from collections import Counter
from dataclasses import dataclass
from functools import cached_property
from enum import Enum
from typing import Self

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

    def __lt__(self, other: Self) -> bool:
        if self.type == other.type:
            return self.card_values < other.card_values
        return self.type.value < other.type.value

    @cached_property
    def counter(self) -> Counter[str]:
        return Counter(self.cards)

    @cached_property
    def card_values(self) -> list[int]:
        return [CARD_RANKS[card] for card in self.cards]

    @cached_property
    def type(self) -> HandType:
        if len(self.counter) == 1:
            return HandType.FIVE_OF_A_KIND
        if len(self.counter) == 2:
            for count in self.counter.values():
                if count in (1, 4):
                    return HandType.FOUR_OF_A_KIND
                return HandType.FULL_HOUSE
        if len(self.counter) == 3:
            for count in self.counter.values():
                if count == 3:
                    return HandType.THREE_OF_A_KIND
            return HandType.TWO_PAIR
        if len(self.counter) == 4:
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD


def main():
    with open('data/day07.txt') as f:
        hands: list[Hand] = []
        for line in f:
            cards, bid, = line.strip().split(' ')
            hands.append(Hand(cards, int(bid)))

    hands.sort()
    winnings = sum(hand.bid * i for i, hand in enumerate(hands, 1))
    print(f'Part 1: {winnings}')


if __name__ == '__main__':
    main()
