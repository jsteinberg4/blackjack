from blackjack import utils
from blackjack.agents import Agent
from blackjack.core import Action, GameState


class Dealer(Agent):
    """
    When the dealer has served every player, the dealers face-down card is turned up.
    If the total is 17 or more, it must stand. If the total is 16 or under, they must take a card.
    The dealer must continue to take cards until the total is 17 or more, at which point the dealer must stand.
    If the dealer has an ace, and counting it as 11 would bring the total to 17 or more (but not over 21),
    the dealer must count the ace as 11 and stand. The dealer's decisions, then, are automatic on all plays,
    whereas the player always has the option of taking one or more cards.

    Dealer Algorithm
    procedure DealerAction
        Input: hand // list of cards
        total <-- sum(hand)
        if total >= 17:
            return "Stand"
        else: // total <= 16
            if Ace in hand:
                ...
            do
                next_card <-- Hit()
                hand <-- hand + next_card
                total <-- total + next_card
            while total < 17

            return "Stand"
    """

    def pick_action(self, game_state: GameState, *args, **kwargs) -> Action:
        """Selects an action using casino rules."""
        act: Action = ...
        hand = game_state.agent_hand(self._is_player)

        if utils.hand_value(hand) >= 17:
            act = Action.STAND
        else:
            act = Action.HIT

        return act
