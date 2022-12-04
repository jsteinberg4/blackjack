from abc import ABC, abstractmethod

from blackjack.core import GameState


class Agent(ABC):
    """
    An agent within the Blackjack Game. Subclasses must implement the `pick_action` method.

    Instance variables:
    -- Agent.is_player: bool -- True if this agent represents the "Player" (e.g. AI Agent, Human player, etc.)
                                 False if this agent represents the "House"/"Dealer"
                                 (Allows Agents to be used as either the Player or Dealer)
    """

    def __init__(self, is_player: bool, *args, **kwargs):
        """
        :param is_player: Required. True for the "Player", False for the "dealer".
        See Agent docstring for more details.
        """
        self._is_player = is_player

    @abstractmethod
    def pick_action(self, game_state: GameState, *args, **kwargs):
        pass
