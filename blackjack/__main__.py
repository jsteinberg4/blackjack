"""
Main Blackjack module. Defines the CLI for running the game.
"""
import argparse
from datetime import datetime

from tqdm import tqdm

from blackjack import Blackjack


def sample(game: Blackjack, n_games: int = 1, sample_size: int = 100):
    """Runs performance testing for a given game"""
    setattr(game, "_verbose", False)

    total_wins = 0
    start = datetime.now()
    for __ in tqdm(range(sample_size)):
        score = game.play(rounds=n_games)
        if score > 0:
            total_wins += 1
    end = datetime.now()
    win_rate = total_wins / sample_size
    # win_rate = sum([win / sample_size for win in wins]) / 10

    print("-" * 50)
    print("Sample Distribution:")
    print("Number of Samples: ", sample_size)
    print("Number of Games per Sample: ", n_games)
    print("Total Games won: ", total_wins)
    print(f"Win Rate: {win_rate: .2%}")
    print("Time elapsed (seconds): ", (end - start).seconds)


def _parse():
    parser = argparse.ArgumentParser(
        prog="python3 -m blackjack",
        description=(
            "A command-line Blackjack game with AI agents. "
            "Final project for CS 4100 Artificial Intelligence by Jesse Steinberg & Deion Smith."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument(
        choices=["test", "run"],
        default="run",
        dest="mode",
        help="Mode: test = Run performance testing, run = Play blackjack with agents",
    )
    parser.add_argument(
        "--player",
        choices=Blackjack.agent_types(),
        type=str,
        default="user",
        dest="player",
        help="Agent type for the user/player",
        nargs="?",
    )
    parser.add_argument(
        "--dealer",
        choices=Blackjack.agent_types(),
        type=str,
        default="casino",
        dest="dealer",
        nargs="?",
        help="Agent type for the dealer.",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        help="Number of full games to run when testing. Used with mode=test.",
        nargs="?",
        dest='sample_size',
        default=1_000,
    )
    parser.add_argument(
        '--hands',
        help="Number of hands to play per sampled game (mode=test). If -1 in mode=Run, will play endless mode..",
        default=-1,
        type=int,
        nargs="?",
        dest='hands',
    )

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = _parse()
    game = Blackjack(
            player=args.get('player'),
            dealer=args.get('dealer'),
        )

    if args['mode'] == 'run':
        hands = args.get('hands')
        if hands < 0:
            game.play(endless=True)
        else:
            game.play(rounds=hands)

    elif args['mode'] == 'test':
        sample(
            game,
            n_games=max(args.get('hands'), 1),
            sample_size=args.get('sample_size', 1_000),
        )
    else:  # Fallback on endless mode with default settings
        game.play(endless=True)
