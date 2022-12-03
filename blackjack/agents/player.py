from abc import ABC, abstractmethod

from blackjack.core.gamestate import GameState


class Player(ABC):

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def pick_action(self, game_state: GameState):
        pass
