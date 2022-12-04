from enum import Enum
from functools import partialmethod


class Action(Enum):
    """
    All possible actions in a game of blackjack
    """
    HIT = "hit"
    STAND = "stand"
    DOUBLE_DOWN = "double-down"
    SURRENDER = "surrender"
    SPLIT = "split"

    def _str(self):
        return self.name

    __str__ = partialmethod(_str)
    __repr__ = partialmethod(_str)
