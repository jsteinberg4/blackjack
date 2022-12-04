from blackjack.agents import Agent
from blackjack.core import GameState, Action


class SingleActionAgent(Agent):
    """An agent which will always pick the same action. If that action is not available,
    it will Stand instead.
    """

    def __init__(self, is_player: bool, action: Action, *args, **kwargs):
        super(SingleActionAgent, self).__init__(is_player)
        self._action = action

    def pick_action(self, game_state: GameState, *args, **kwargs):
        """Returns SingleActionAgent.action if allowed, otherwise Stands"""
        legal_actions = game_state.actions(self._is_player)

        if self._action in legal_actions:
            return self._action
        return Action.STAND
