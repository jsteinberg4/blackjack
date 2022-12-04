from __future__ import annotations

from functools import partialmethod

from blackjack import utils
from blackjack.core import Action, Card


class GameState:
    """
    Immutable representation of the game state.

    The visible dealer hand, player's hand, and current score.
    """

    def __init__(
        self,
        dealer_hand: list[Card],
        player_hand: list[Card],
        player_score: int,
        hide_dealer: bool = True,
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

    def agent_hand(self, is_player: bool) -> list[Card]:
        hand = self._player_hand if is_player else self._dealer_hand
        return hand.copy()

    @property
    def dealer(self) -> list[Card]:
        """Returns a copy of the dealer's hand"""
        return self.agent_hand(False)

    @property
    def hand(self) -> list[Card]:
        """Returns a copy of the player's hand"""
        return self.agent_hand(True)

    @property
    def score(self):
        """Get current score"""
        return self._score

    def actions(self, is_player: bool) -> list[Action]:
        """List of legal actions for the given agent"""
        # Note -- Players can technically hit at any value
        legal_actions = [Action.HIT, Action.STAND]
        hand = self.agent_hand(is_player)

        # -- Double Down: only on first hit
        # -- Split: If first hit AND hand contains 2 of the same card
        if len(hand) == 2:
            legal_actions.append(Action.DOUBLE_DOWN)
            if hand[0].value is hand[1].value:
                legal_actions.append(Action.SPLIT)

        # -- Surrender: Players can forfeit for a slightly less negative score
        if is_player:
            legal_actions.append(Action.SURRENDER)

        return legal_actions

    def _display(self) -> str:
        """String representation of the game"""
        dealer_score = (
            "\n" if self._hide_dealer else f" -- {utils.hand_value(self.dealer)}\n"
        )
        return (
            "-" * 20
            + "\n"
            + f"Dealer Hand: {self.dealer}"
            + dealer_score
            + f"Your Hand: {self.hand} -- {utils.hand_value(self.hand)}\n"
            + f"Score: {self.score}\n"
        )

    __repr__ = partialmethod(_display)
    __str__ = partialmethod(_display)
