from collections import abc
from functools import partialmethod
from pprint import pformat
import random

from blackjack.core import Card, Suit


class StandardDeck(abc.Sequence):
    """
    Represents a deck of 52 playing cards
    """

    def __init__(self, *, decks: int = 1, **kwargs):
        self._cards = self._create_deck(decks)
        self.shuffle()

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, item: int | slice) -> Card | list[Card]:
        return self._cards[item]

    def __string(self) -> str:
        return "Deck(" + pformat(self._cards, compact=True, width=100) + ")"
    __str__ = partialmethod(__string)
    __repr__ = partialmethod(__string)

    @staticmethod
    def _create_deck(decks: int = 1):
        deck = []
        # Allow for multiple decks to be combined
        for _ in range(decks):
            for s in Suit:
                deck.extend(Card.full_suit(s))
        return deck

    def shuffle(self):
        """Randomly shuffle the cards within this deck."""
        random.shuffle(self._cards)
