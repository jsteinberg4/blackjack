from __future__ import annotations

from typing import Callable, Iterator

from blackjack import utils
from blackjack.agents.agents import UserPlayer, RandomPlayer
from blackjack.core.card import Card, Action
from blackjack.agents.dealer import Dealer
from blackjack.core.gamestate import GameState
from blackjack.agents.player import Player
from blackjack.core.standard_deck import StandardDeck


class BlackJack:
    """
    Represents a running game of blackjack
    """

    __PLAYERS = {"user": UserPlayer, "random": RandomPlayer}
    __DEALERS = {"casino": Dealer}

    @classmethod
    def __player(cls, p: str, default: str = "user") -> Callable[[], Player]:
        return cls.__PLAYERS.get(p, cls.__PLAYERS[default])

    @classmethod
    def __dealer(cls, d: str, default: str = "casino") -> Callable[[], Dealer]:
        return cls.__DEALERS.get(d, cls.__DEALERS[default])

    def __init__(
        self,
        *,
        player: str = None,
        dealer: str = None,
        verbose: bool = True,
        **kwargs,
    ):
        # TODO -- Docstring
        self._deck = self._make_endless_deck(StandardDeck())
        self._dealer = self.__dealer(dealer)()  # Dealer vars
        self._dealer_hand = []
        self._hide_dealer = True
        self._player = self.__player(player)()  # Player vars
        self._player_hand = []
        self._score = 0
        self._verbose = verbose

    @property
    def score(self) -> int:
        """Score of the most recently completed/running game"""
        return self._score

    def _clear_hands(self) -> None:
        self._dealer_hand = []
        self._player_hand = []

    def _init_hands(self) -> None:
        self._clear_hands()
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
            self._hide_dealer = True
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

        Score:
        +1.5 -- Player gets blackjack (Ace + Face card)
        +1 -- Player Wins
        +0 -- Push (draw)
        -1 -- Dealer Wins
        """
        player_sum = utils.hand_value(self._player_hand)
        dealer_sum = utils.hand_value(self._dealer_hand)
        player_bust = player_sum > 21
        dealer_bust = dealer_sum > 21
        score = 0

        match (player_bust, dealer_bust):
            case False, False:  # Neither bust, closest to 21 wins
                player_dist = abs(21 - player_sum)
                dealer_dist = abs(21 - dealer_sum)

                # 1) Somebody could have blackjack
                # 2) Players have equal hands
                # 3) Nobody has blackjack. Whoever is closer to 21 wins
                if player_dist == dealer_dist:  # Equal hands always push
                    score = 0

                # Neither player has bust. Players do not have equal hands
                elif player_dist == 0:  # Player got blackjack
                    score = 1.5 if utils.blackjack_hand(self._player_hand) else 1

                if player_dist == dealer_dist:  # 2
                    score = 0
                elif player_dist == 0 or dealer_dist == 0:  # 1

                else:  # 3
                    score = +1 if player_dist < dealer_dist else -1
            case True, False:  # Only player bust, dealer wins
                score = -1
            case False, True:  # Only dealer bust, player wins
                score = +1
            case True, True:  # Both bust, push
                score = 0

        return score

    def _act_or_stand(self, hand: list[Card], action: Action) -> bool:
        """return True if player chose to Stand, False otherwise"""
        match action:
            case Action.STAND:
                return True
            case Action.HIT:
                hand.append(next(self._deck))
            case _:
                raise ValueError("Invalid action: ", action)

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
        if utils.hand_value(self._player_hand) < utils.BLACKJACK:
            #   Until dealer stands or busts:
            while not stand and utils.hand_value(self._dealer_hand) < utils.BLACKJACK:
                # Let dealer choose legal move
                action = self._dealer.pick_action(self.state())
                stand = self._act_or_stand(self._dealer_hand, action)

        # score round
        return self._score_hands()
