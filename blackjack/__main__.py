import sys
from datetime import datetime

from tqdm import tqdm

from blackjack.core.blackjack import BlackJack


def info() -> None:
    usage = (
        "Blackjack\n"
        "Usage: ..."
    )
    print(usage)


def sample(game: BlackJack, n_samples: int = 10, sample_size: int = 100, iters: int = 10):
    setattr(game, '_verbose', False)

    start = datetime.now()
    sample_data = []
    for __ in range(iters):
        scores = []
        for _ in tqdm(range(n_samples)):
            game.play(sample_size)
            scores.append(game.score)
        sample_data.append(sum([1 if score > 0 else 0 for score in scores]) / n_samples)
    end = datetime.now()

    print('-'*50)
    print("Sample Distribution:")
    print("Sampling Rounds: ", iters)
    print("Num Samples: ", samples)
    print("Num Games per Sample: ", sample_size)
    print("Sample mean: ", sum(sample_data) / samples)
    print("Time elapsed (seconds): ", (end - start).seconds)


def run_default():
    BlackJack(player='user').play(endless=True)


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
        if 'sample' in sys.argv:
            samples = 100  # TODO -- samples, rounds should be CLI params
            rounds = 10_000
            iterations = 2
            player = ...  # TODO -- Param for player agent
            dealer = ...  # TODO -- Param for dealer agent
            sample(BlackJack(), n_samples=samples, sample_size=rounds, iters=iterations)
        else: # TODO -- Other params
            BlackJack().play(10)
