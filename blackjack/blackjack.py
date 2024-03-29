from __future__ import annotations

from functools import partial
from typing import Callable, Iterator

from blackjack import utils
from blackjack.agents import Agent, Dealer, RandomAgent, UserAgent, SingleActionAgent
from blackjack.agents.qlearning_agent import QLearningAgent
from blackjack.core import Action, Card, GameState, StandardDeck


class Blackjack:
    """
    Represents a running game of blackjack
    """

    __AGENTS = {
        "user": UserAgent,
        "random": RandomAgent,
        "casino": Dealer,
        "hit": partial(SingleActionAgent, action=Action.HIT),
        "stand": partial(SingleActionAgent, action=Action.STAND),
        "q": QLearningAgent,
    }
    __DEFAULT_PLAYER = "user"
    __DEFAULT_DEALER = "casino"

    @classmethod
    def agent_types(cls) -> tuple[str]:
        """Get a list of all permitted agents. Mostly exists for CLI options."""
        return tuple(cls.__AGENTS.keys())

    @classmethod
    def __agent(cls, a: str, default: str = "random") -> Callable[[bool], Agent]:
        """Gets the appropriate agent type"""
        return cls.__AGENTS.get(a, cls.__AGENTS[default])

    def __init__(
        self,
        *,
        player: str = None,
        dealer: str = None,
        verbose: bool = True,
        train_rounds: int = 10_000,
        **kwargs,
    ):
        # TODO -- Docstring
        self._deck = self._make_endless_deck(StandardDeck())
        self._score = 0
        self._verbose = verbose
        self._train_rounds = train_rounds

        # Game Settings
        self._hide_dealer = True
        self._split_hands = False
        self._surrender = False
        self._multiplier = 1.0  # Score multiplier for doubling down, surrendering

        # Dealer Vars
        self._dealer = self.__agent(dealer, default=self.__DEFAULT_DEALER)(
            is_player=False
        )
        self._dealer_hand = []

        # Player vars
        self._player = self.__agent(player, default=self.__DEFAULT_PLAYER)(
            is_player=True
        )
        self._player_hand = []
        if self._player.trainable:
            self._train(self._player)

        print(self._player._states)



    def _train(self, player):
        for _ in range(self._train_rounds):
            self._init_hands()
            stand = False
            while not stand and utils.hand_value(self._player_hand) < utils.BLACKJACK:
                state = self.state()
                action = self._player.pick_action(state)
                stand = self._act_or_stand(self._player_hand, action)
                next_state = self.state()
                self._player.observe_transition(state, action, next_state, 21 - utils.hand_value(self._player_hand))

            stand = False
            self._hide_dealer = False
            if utils.hand_value(self._player_hand) <= utils.BLACKJACK:
                #   Until dealer stands or busts:
                while not stand and utils.hand_value(self._dealer_hand) < utils.BLACKJACK:
                    # Let dealer choose legal move
                    action = self._dealer.pick_action(self.state())
                    stand = self._act_or_stand(self._dealer_hand, action)
            self._reset_hand()


    def _reset_hand(self):
        """Reset between rounds"""
        self._hide_dealer = True
        self._multiplier = 1.0
        self._surrender = False
        self._split_hands = False
        self._dealer_hand = []
        self._player_hand = []

    @property
    def score(self) -> int:
        """Score of the most recently completed/running game"""
        return self._score

    def _init_hands(self) -> None:
        for x in range(4):
            if x % 2 == 0:
                self._dealer_hand.append(next(self._deck))
            else:
                self._player_hand.append(next(self._deck))

    @staticmethod
    def _make_endless_deck(d: StandardDeck) -> Iterator[Card]:
        card_idx = 0
        while True:
            if card_idx >= len(d):
                card_idx = 0
                d.shuffle()
            yield d[card_idx]
            card_idx += 1

    def state(self) -> GameState:
        """Returns an external representation of the current game."""
        dealer = (
            ["<HIDDEN>", *self._dealer_hand[1:]]
            if self._hide_dealer
            else self._dealer_hand
        )

        return GameState(
            dealer, self._player_hand, self._score, hide_dealer=self._hide_dealer
        )

    def play(self, rounds: int = 10, endless: bool = False) -> int:
        """Play N hands of blackjack against a dealer.

        :param rounds: Fixed # of rounds to play
        :param endless: Run forever
        :return: player's final score
        """

        def runner():
            self._reset_hand()
            self._score += self._next_round()

            if self._verbose:
                print(self.state())

        self._score = 0
        if endless:
            while True:
                runner()
        else:
            for _ in range(rounds):
                runner()

        return self._score

    def _score_hands(self) -> int:
        """Score the player/dealer hands

        Score (multiply by self._multiplier):
        +1.5 -- Player gets blackjack (Ace + Face card)
        +1 -- Player Wins
        +0 -- Push (draw)
        -0.5 -- Player Surrender
        -1 -- Dealer Wins
        """
        if self._surrender:
            return -0.5

        player_sum = utils.hand_value(self._player_hand)
        dealer_sum = utils.hand_value(self._dealer_hand)
        player_bust = player_sum > 21
        dealer_bust = dealer_sum > 21
        score = 0

        # Score based on who bust
        match (player_bust, dealer_bust):
            case False, False:  # Neither bust, closest to 21 wins
                player_dist = abs(21 - player_sum)
                dealer_dist = abs(21 - dealer_sum)

                # See who scored closest to 21
                if player_dist == dealer_dist:  # Equal hands always push
                    score = 0
                elif dealer_dist < player_dist:  # Dealer won the hand
                    score = -1
                else:  # Player won the hand
                    # Bonus points for blackjack
                    score = 1.5 if utils.blackjack_hand(self._player_hand) else 1
            case True, False:  # Only player bust, dealer wins
                score = -1
            case False, True:  # Only dealer bust, player wins
                score = +1
            case True, True:  # Both bust, push
                score = 0

        return score * self._multiplier

    def _act_or_stand(self, hand: list[Card], action: Action) -> bool:
        """return True if player chose to Stand, False otherwise"""
        match action:
            case Action.STAND:
                return True
            case Action.HIT:
                hand.append(next(self._deck))
            case Action.SURRENDER:
                self._surrender = True
                return True
            case Action.DOUBLE_DOWN:
                # TODO -- Double score?
                self._multiplier = 2
                hand.append(next(self._deck))
            case Action.SPLIT:
                # TODO -- Split hand?
                self._split_hands = True
            case _:
                raise ValueError("Invalid action: ", action)
        return False

    def _next_round(self) -> int:
        # Start the round by dealing 2 cards to dealer & player, alternating
        self._init_hands()

        # Until player stands or busts:
        stand = False
        while not stand and utils.hand_value(self._player_hand) < utils.BLACKJACK:
            # Let player choose valid move
            action = self._player.pick_action(self.state())
            stand = self._act_or_stand(self._player_hand, action)

        # If player did not "Bust", then the dealer plays
        self._hide_dealer = False
        stand = False
        if utils.hand_value(self._player_hand) <= utils.BLACKJACK:
            #   Until dealer stands or busts:
            while not stand and utils.hand_value(self._dealer_hand) < utils.BLACKJACK:
                # Let dealer choose legal move
                action = self._dealer.pick_action(self.state())
                stand = self._act_or_stand(self._dealer_hand, action)

        # score round
        return self._score_hands()
