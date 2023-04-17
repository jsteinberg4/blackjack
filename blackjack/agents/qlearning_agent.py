import random

from blackjack import utils
from blackjack.agents import Agent
from blackjack.core import GameState, Action


class QLearningAgent(Agent):
    def __init__(
        self,
        is_player: bool,
        *args,
        alpha: float = 1.0,
        epsilon: float = 0.05,
        gamma: float = 0.8,
        num_training: int = 10,
        **kwargs
    ):
        super().__init__(is_player, trainable=True, *args, **kwargs)
        self._alpha = alpha
        self._epsilon = epsilon
        self._gamma = gamma
        self._num_training = num_training

        self._states = dict()  # Dict of {(hand_value, action): reward)

    def observe_transition(
        self,
        state: GameState,
        action: Action,
        next_state: GameState,
        delta_reward: float,
    ):
        legal_actions = state.actions(self._is_player)
        hand_value = utils.hand_value(state.hand)
        max_next_action = max([self._states.get((hand_value, a), float('-inf')) for a in legal_actions])
        val_current = self._states.get((hand_value, action), 0)

        self._states[(hand_value, action)] = val_current + self._alpha*(delta_reward + self._gamma*max_next_action - val_current)

    def pick_action(self, game_state: GameState, *args, **kwargs):
        max_action_val = float('-inf')
        max_action = None
        state = utils.hand_value(game_state.hand)
        actions = game_state.actions(self._is_player)
        if random.random() < self._epsilon:
            return random.choice(actions)
        else:
            for action in actions:
                qval = self._states.get((state, action))
                if qval is None:
                    self._states[(state, action)] = 0
                else:
                    max_action, max_action_val = max([(max_action, max_action_val), (action, qval)], key=lambda t: t[1])

            # No action got chosen for some reason
            if max_action is None:
                max_action = random.choice(actions)
            return max_action