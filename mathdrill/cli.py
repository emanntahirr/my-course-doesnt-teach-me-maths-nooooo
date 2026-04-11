import argparse
from mathdrill.engine import run_drill
from mathdrill.questions import CATEGORIES
from mathdrill.stats import show_stats


def main():
    parser = argparse.ArgumentParser(
        description="terminal math drills for competitive coding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="categories: " + ", ".join(CATEGORIES.keys()),
    )
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=5,
        help="number of questions (default: 5)",
    )
    parser.add_argument(
        "-d", "--difficulty",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="difficulty 1-3 (default: 1)",
    )
    parser.add_argument(
        "-c", "--category",
        type=str,
        choices=list(CATEGORIES.keys()),
        default=None,
        help="focus on a specific category",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="view your practice history and streak",
    )
    parser.add_argument(
        "--adaptive",
        action="store_true",
        help="auto-scale difficulty based on how you're doing",
    )

    args = parser.parse_args()

    if args.stats:
        show_stats()
        return

    run_drill(
        num_questions=args.num,
        difficulty=args.difficulty,
        category=args.category,
        adaptive=args.adaptive,
    )


if __name__ == "__main__":
    main()
