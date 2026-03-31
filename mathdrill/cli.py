import argparse
from mathdrill.engine import run_drill
from mathdrill.questions import CATEGORIES


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

    args = parser.parse_args()
    run_drill(
        num_questions=args.num,
        difficulty=args.difficulty,
        category=args.category,
    )


if __name__ == "__main__":
    main()
