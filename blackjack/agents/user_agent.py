from blackjack.agents import Agent
from blackjack.core import Action, GameState


class UserAgent(Agent):
    """
    An agent acts according to user input.
    """

    def pick_action(self, game_state: GameState, *args, **kwargs):
        actions = [str(a).lower() for a in game_state.actions(agent=self._is_player)]
        actions_str = ", ".join(actions)

        print(game_state)
        while (
            choice := input("Select one of [" + actions_str + "]: ").lower()
        ) not in actions:
            print(choice, choice not in actions)
            print(actions)
            print("Please enter one of the given values.")

        return Action(choice)
