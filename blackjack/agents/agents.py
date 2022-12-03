import random

from blackjack.core import card
from blackjack.core.gamestate import GameState
from blackjack.agents.player import Player


class UserPlayer(Player):
    def pick_action(self, game_state: GameState):
        actions = [str(a).lower() for a in game_state.actions()]
        actions_str = ", ".join(actions)

        print(game_state)
        while (
            choice := input("Select one of [" + actions_str + "]: ").lower()
        ) not in actions:
            print(choice, choice not in actions)
            print(actions)
            print("Please enter one of the given values.")

        return card.Action(choice)


class RandomPlayer(Player):
    def pick_action(self, game_state: GameState):
        actions = game_state.actions()
        return random.choice(actions)
