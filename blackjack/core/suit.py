from __future__ import annotations

from enum import Enum, auto
from functools import partialmethod


class Suit(Enum):
    """Enumerates all 4 possible suits for a standard deck of cards
    """
    CLUBS = auto()
    SPADES = auto()
    HEARTS = auto()
    DIAMONDS = auto()

    def __name_str(self) -> str:
        return self.name.capitalize()

    __repr__ = partialmethod(__name_str)
    __str__ = partialmethod(__name_str)
