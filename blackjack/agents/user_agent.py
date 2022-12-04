from blackjack.agents import Agent
from blackjack.core import Action, GameState


class UserAgent(Agent):
    """
    An agent acts according to user input.
    """

    def pick_action(self, game_state: GameState, *args, **kwargs):
        legal_actions = game_state.actions(is_player=self._is_player)
        action: Action = None

        print(game_state)
        print("Select one of the following: ")
        for opt, act in enumerate(legal_actions):
            print(opt + 1, ") ", act, sep="")

        # Repeatedly prompt until a valid option is selected
        while action is None:
            choice = input("Enter the option number: ")
            try:
                choice_num = int(choice) - 1
                if choice_num in range(len(legal_actions)):
                    action = legal_actions[choice_num]
                else:
                    print("Invalid option. Choice must be in range: [1...", len(legal_actions), "].", sep="")
            except ValueError:
                continue

        return action
