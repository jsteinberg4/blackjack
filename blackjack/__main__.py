"""
Main Blackjack module. Defines the CLI for running the game.
"""

import sys
from datetime import datetime

from tqdm import tqdm

from blackjack import Blackjack


def info() -> None:  # TODO
    """Prints the usage instructions"""
    usage = (
        "Blackjack\n"
        "Usage: ..."
    )
    print(usage)


def sample(game: Blackjack, n_games: int = 1, sample_size: int = 100):
    """Runs performance testing for a given game"""
    setattr(game, '_verbose', False)

    # total_wins = 0
    wins = []
    start = datetime.now()
    for _ in range(10):
        total_wins = 0
        for __ in tqdm(range(sample_size)):
            score = game.play(rounds=n_games)
            if score > 0:
                total_wins += 1
        wins.append(total_wins)
    end = datetime.now()
    # win_rate = total_wins / sample_size
    win_rate = sum([win / sample_size for win in wins]) / 10

    print('-'*50)
    print("Sample Distribution:")
    print("Number of Samples: ", sample_size)
    print("Number of Games per Sample: ", n_games)
    # print("Total Games won: ", total_wins)
    print("Sample mean: ", win_rate)
    print("Time elapsed (seconds): ", (end - start).seconds)


def run_default():
    """Runs a game with the default parameters"""
    Blackjack(player='user').play(endless=True)


if __name__ == '__main__':
    # Exit for program description
    if '-h' in sys.argv or '--help' in sys.argv:
        info()
        sys.exit(1)

    # TODO -- Commandline interface
    if len(sys.argv) == 1:
        run_default()
    else:
        # TODO -- Parameters for sampling
        if 'sample' == sys.argv[1]:
            # TODO -- should be CLI params
            sample_size = 1_000
            n_games = 10
            player = 'random'
            dealer = 'random'
            sample(Blackjack(player=player, dealer=dealer), n_games=n_games, sample_size=sample_size)
        elif "play" == sys.argv[1]:
            player = 'user'  # TODO -- CLI params
            dealer = 'casino'
            Blackjack(player=player, dealer=dealer).play(endless=True)
        else:  # TODO -- Other params
            Blackjack().play(10)
