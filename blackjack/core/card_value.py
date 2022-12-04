from __future__ import annotations

from functools import partialmethod

import aenum


class CardValue(aenum.IntEnum):
    """Blackjack card values"""
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
