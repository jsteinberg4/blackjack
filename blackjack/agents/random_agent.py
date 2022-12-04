import random

from blackjack.agents import Agent
from blackjack.core import GameState


class RandomAgent(Agent):
    """
    An agent which picks actions at random.
    """

    def pick_action(self, game_state: GameState, *args, **kwargs):
        actions = game_state.actions(agent=self._is_player)
        return random.choice(actions)
