from __future__ import annotations

__all__ = [
    "Suit",
    "Action",
    "CardValue",
    "Card",
]

from dataclasses import dataclass, field
from enum import Enum, auto
from functools import partialmethod
from typing import Any

import aenum


class Action(Enum):
    HIT = "hit"
    STAND = "stand"

    def _str(self):
        return self.name
    __str__ = partialmethod(_str)
    __repr__ = partialmethod(_str)


class Suit(Enum):
    CLUBS = auto()
    SPADES = auto()
    HEARTS = auto()
    DIAMONDS = auto()

    def __name_str(self) -> str:
        return self.name.capitalize()
    __repr__ = partialmethod(__name_str)
    __str__ = partialmethod(__name_str)


class CardValue(aenum.IntEnum):
    # https://stackoverflow.com/questions/31537316/python-enums-with-duplicate-values
    _settings_ = aenum.NoAlias

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10
    ACE = 11

    def __name_str(self) -> str:
        return self.name.capitalize()

    __repr__ = partialmethod(__name_str)
    __str__ = partialmethod(__name_str)



@dataclass(frozen=True, order=True, slots=True)
class Card:
    """
    An immutable representation of a playing card.
    """

    value: CardValue = field(compare=True)
    suit: Suit = field(compare=False)

    def __init__(self, value: int | CardValue, suit: Suit):
        object.__setattr__(self, "value", CardValue(value) if isinstance(value, int) else value)
        object.__setattr__(self, "suit", suit)

    @classmethod
    def full_suit(cls, suit: Suit) -> list[Card]:
        """Creates an ordered list of all cards for the given suit"""
        return [Card(v, suit) for v in CardValue]

    def is_face(self) -> bool:
        """Returns true if this card is a Face card, False otherwise"""
        return self.value in {CardValue.JACK, CardValue.QUEEN, CardValue.KING}

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
