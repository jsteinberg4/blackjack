from __future__ import annotations

from typing import Callable, Iterator

from blackjack.core import constants
from blackjack.core.card import Card, Action
from blackjack.core.dealer import Dealer
from blackjack.core.gamestate import GameState
from blackjack.core.player import Player
from blackjack.core.agents import UserPlayer, RandomPlayer
from blackjack.core.standard_deck import StandardDeck


class BlackJack:
    """
    Represents a running game of blackjack
    """
    __PLAYERS = {'user': UserPlayer, 'random': RandomPlayer}
    __DEALERS = {'casino': Dealer}
    __DECKS = {'standard': StandardDeck}

    @classmethod
    def __player(cls, p: str, default: str = 'user') -> Callable[[], Player]:
        return cls.__PLAYERS.get(p, cls.__PLAYERS[default])

    @classmethod
    def __dealer(cls, d: str, default: str = 'casino') -> Callable[[], Dealer]:
        return cls.__DEALERS.get(d, cls.__DEALERS[default])

    @classmethod
    def __deck(cls, deck: str, default: str = 'standard') -> Callable[[], StandardDeck]:
        return cls.__DECKS.get(deck, cls.__DECKS[default])

    def __init__(self, *, player: str = None, dealer: str = None, deck: str = None, verbose: bool = True, **kwargs):
        # TODO -- Docstring
        self._deck = self.__deck(deck)()
        self._endless_deck = self._make_endless_deck(self._deck)
        self._dealer = self.__dealer(dealer)()
        self._dealer_hand = []
        self._player = self.__player(player)()
        self._player_hand = []
        self._card_idx = 0
        self._score = 0
        self._hide_dealer = True
        self._verbose = verbose

    @property
    def score(self) -> int:
        """Score of the most recently completed/running game"""
        return self._score


    def _next_card(self):
        return next(self._endless_deck)

    def _clear_hands(self) -> None:
        self._dealer_hand = []
        self._player_hand = []

    def _init_hands(self) -> None:
        self._clear_hands()
        for x in range(4):
            if x % 2 == 0:
                self._dealer_hand.append(self._next_card())
            else:
                self._player_hand.append(self._next_card())

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
        dealer = ['<HIDDEN>', *self._dealer_hand[1:]] if self._hide_dealer else self._dealer_hand

        return GameState(dealer,
                         self._player_hand,
                         self._score, hide_dealer=self._hide_dealer)

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
        +1 -- Player Wins
        +0 -- Push (draw)
        -1 -- Dealer Wins
        """
        player_sum = sum(self._player_hand)
        dealer_sum = sum(self._dealer_hand)
        player_bust = player_sum > 21
        dealer_bust = dealer_sum > 21
        score = 0

        match (player_bust, dealer_bust):
            case False, False:  # Neither bust, closest to 21 wins
                player_dist = abs(21 - player_sum)
                dealer_dist = abs(21 - dealer_sum)
                score = +1 if player_dist < dealer_dist else -1
            case True, False:   # Only player bust, dealer wins
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
                hand.append(self._next_card())
            case _:
                raise ValueError("Invalid action: ", action)

    def _next_round(self) -> int:
        # Start the round by dealing 2 cards to dealer & player, alternating
        self._init_hands()

        # Until player stands or busts:
        stand = False
        while not stand and sum(self._player_hand) < constants.BLACKJACK:
            # Let player choose valid move
            action = self._player.pick_action(self.state())
            stand = self._act_or_stand(self._player_hand, action)

        # If player did not "Bust", then the dealer plays
        self._hide_dealer = False
        stand = False
        if sum(self._player_hand) < constants.BLACKJACK:
            #   Until dealer stands or busts:
            while not stand and sum(self._dealer_hand) < constants.BLACKJACK:
                # Let dealer choose legal move
                # action = self._dealer.pick_action(self.state())
                action = Action.HIT
                stand = self._act_or_stand(self._dealer_hand, action)

        # score round
        return self._score_hands()
