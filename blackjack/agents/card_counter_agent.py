from blackjack.agents import Agent
from blackjack.core import Action, Card, GameState, CardValue


class CardCounterAgent(Agent):
    """
    Agent which keeps track of all seen cards to make a
    probabilistic guess about possible successive hands.
    """

    def __init__(self, is_player: bool, num_decks: int = 1, *args, **kwargs):
        super(CardCounterAgent, self).__init__(is_player)
        self._seen: set[Card] = set()
        self._total_cards = 52 * num_decks
        self._remaining = {value.name: 4 * num_decks for value in CardValue}

    def _num_unseen(self) -> int:
        """Count the number of cards still unseen"""
        return self._total_cards - len(self._seen)

    def pick_action(self, game_state: GameState, *args, **kwargs) -> Action:
        actions = game_state.actions(self._is_player)
        max_action: Action = ...

        # Keep track of what cards have been seen so far
        if len(game_state.dealer) == len(game_state.hand) == 2:  # First action this round
            for card in [*game_state.dealer, *game_state.hand]:
                self._seen.add(card)
                self._remaining[card.value] = self._remaining[card.value] - 1
        else:
            for card in game_state.hand[2:]:
                self._seen.add(card)
                self._remaining[card.value] = self._remaining[card.value] - 1

        for action in actions:
            continue

        return max_action

    def _expected(self, game_state, action) -> float:
        # TODO -- Compute probability of a hand with value <= 21
        pass