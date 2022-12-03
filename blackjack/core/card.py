from __future__ import annotations

__all__ = [
    "Suit",
    "Action",
    "CardValue",
    "Card",
]

from dataclasses import dataclass, field
from enum import Enum, auto, IntEnum
from functools import partialmethod
from typing import Any


class SimpleName(Enum):
    def __name_str(self) -> str:
        return self.name.capitalize()

    def __repr__(self) -> str:
        return self.__name_str()

    def __str__(self) -> str:
        return self.__name_str()


class Action(Enum):
    HIT = "hit"
    STAND = "stand"

    def _str(self):
        return self.name

    __str__ = partialmethod(_str)
    __repr__ = partialmethod(_str)


class Suit(SimpleName):
    CLUBS = auto()
    SPADES = auto()
    HEARTS = auto()
    DIAMONDS = auto()


class CardValue(SimpleName, IntEnum):
    # NOTE :: Inherits from SimpleName **first**. Any methods defined in SimpleName will
    #         be discovered and used first.
    ACE = 11
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


@dataclass(frozen=True, order=True, slots=True)
class Card:
    """
    An immutable representation of a playing card.
    """

    value: CardValue = field(compare=True)
    suit: Suit = field(compare=False)

    def __init__(self, value: int, suit: Suit):
        object.__setattr__(self, "value", CardValue(value))
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
