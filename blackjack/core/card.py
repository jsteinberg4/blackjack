from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from blackjack.core import CardValue, Suit


@dataclass(frozen=True, order=True, slots=True)
class Card:
    """
    An immutable representation of a playing card.
    """

    value: CardValue = field(compare=True)
    suit: Suit = field(compare=False)

    def __init__(self, value: CardValue, suit: Suit):
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "suit", suit)

    @classmethod
    def full_suit(cls, suit: Suit) -> list[Card]:
        """Creates an ordered list of all cards for the given suit"""
        return [Card(v, suit) for v in CardValue]

    def __name_str(self) -> str:
        return f"{self.value} of {self.suit}"

    def __repr__(self) -> str:
        return self.__name_str()

    def __str__(self) -> str:
        return self.__name_str()

    def __add__(self, other: Any) -> int:
        """Adds up the values of 2 cards"""
        if isinstance(other, Card):
            return self.value + other.value
        elif isinstance(other, int):
            return self.value + CardValue(other)
        else:
            raise TypeError(f"Cannot add types: self={type(self)}, other={type(other)}")

    def __radd__(self, other):
        if isinstance(other, int):
            return self.value + other
        else:
            raise TypeError(f"Cannot add types: self={type(self)}, other={type(other)}")
