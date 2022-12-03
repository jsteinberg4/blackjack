from __future__ import annotations

from functools import partialmethod

from blackjack.core import constants
from blackjack.core.card import Card, Action


class GameState:
    """
    Immutable representation of the game state.

    The visible dealer hand, player's hand, and current score.
    """

    def __init__(
        self, dealer_hand: list[Card], player_hand: list[Card], player_score: int, hide_dealer: bool = True
    ):
        """
        Create a GameState.

        :param dealer_hand: the portion of the dealer's hand currently visible to the player
        :param player_hand: the player's cards
        :param player_score: the player's running score
        """
        self._dealer_hand = dealer_hand
        self._player_hand = player_hand
        self._score = player_score
        self._hide_dealer = hide_dealer

    @property
    def dealer(self) -> list[Card]:
        """Returns a copy of the dealer's hand"""
        return self._dealer_hand.copy()

    @property
    def hand(self) -> list[Card]:
        """Returns a copy of the player's hand"""
        return self._player_hand.copy()

    @property
    def score(self):
        """Get current score"""
        return self._score

    @staticmethod
    def hand_value(cards: list[Card]) -> int:
        """Computes the total value of a hand"""
        return sum(cards)

    def actions(self, dealer: bool = False) -> list[Action]:
        """List of legal actions"""
        actions = [Action.STAND]
        if self.hand_value(self.hand) < constants.BLACKJACK:
            actions.append(Action.HIT)
        return actions

    def _display(self) -> str:
        """String representation of the game"""
        dealer_score = '\n' if self._hide_dealer else f' -- {self.hand_value(self.dealer)}\n'
        return ("-"*20 + '\n'
            + f"Dealer Hand: {self.dealer}" + dealer_score
            + f"Your Hand: {self.hand} -- {self.hand_value(self.hand)}\n"
            + f"Score: {self.score}\n"
        )
    __repr__ = partialmethod(_display)
    __str__ = partialmethod(_display)
