import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from mathdrill.questions import random_question, weakspot_question, question_by_type, CATEGORIES
from mathdrill.stats import (
    save_session, save_question_results, streak_message, get_weak_categories,
    update_review_card, get_due_reviews, seed_review_from_history,
)

console = Console()


def _header(round_num, total, score, streak):
    streak_display = f" {streak} 🔥" if streak >= 2 else ""
    return (
        f"[bold cyan]⚡ MATH DRILL[/bold cyan]  —  "
        f"Round {round_num}/{total}  |  "
        f"Score: {score}/{round_num - 1}  |  "
        f"Streak:{streak_display}"
    )


def _check_answer(user_input, question):
    user_input = user_input.strip()
    if question.get("string_answer"):
        return user_input.lower() == str(question["answer"]).lower()
    try:
        return int(user_input) == question["answer"]
    except ValueError:
        return False


def _adapt_difficulty(current, recent_results):
    if len(recent_results) < 3:
        return current
    last_3 = [r["correct"] for r in recent_results[-3:]]
    if all(last_3) and current < 3:
        return current + 1
    if not any(last_3) and current > 1:
        return current - 1
    return current


def run_drill(num_questions=5, difficulty=1, category=None, adaptive=False, weakspot=False):
    console.clear()
    console.print()
    smsg = streak_message()

    weak_cats = None
    if weakspot:
        weak_cats = get_weak_categories()

    mode = "adaptive" if adaptive else f"difficulty {'★' * difficulty}{'☆' * (3 - difficulty)}"
    if weakspot:
        mode += "  •  weak spot targeting"
    console.print(
        Panel(
            "[bold magenta]MATH DRILL[/bold magenta]\n"
            f"[dim]{num_questions} questions  •  "
            f"{mode}  •  "
            f"{'all categories' if not category else category}[/dim]\n"
            f"{smsg}",
            border_style="bright_magenta",
        )
    )

    if weakspot and weak_cats:
        console.print(f"  [dim]focusing on: {', '.join(weak_cats)}[/dim]")
    elif weakspot:
        console.print("  [dim]no weak spots found yet, using all categories[/dim]")
    console.print()

    score = 0
    streak = 0
    best_streak = 0
    current_difficulty = difficulty
    results = []

    for i in range(1, num_questions + 1):
        if adaptive:
            current_difficulty = _adapt_difficulty(current_difficulty, results)

        if weakspot and not category:
            q = weakspot_question(current_difficulty, weak_cats)
        else:
            q = random_question(current_difficulty, category)

        console.rule(style="dim")
        header = _header(i, num_questions, score, streak)
        if adaptive:
            header += f"  |  Difficulty: {'★' * current_difficulty}{'☆' * (3 - current_difficulty)}"
        console.print(header)
        console.print(f"\n  [bold yellow]{q['category']}[/bold yellow]")
        console.print(f"\n  {q['question']}\n")

        start = time.time()
        try:
            answer = console.input("[bold green]> [/bold green]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]quitting...[/dim]")
            return

        elapsed = time.time() - start
        correct = _check_answer(answer, q)
        qt = q.get("question_type", "")

        if correct:
            score += 1
            streak += 1
            best_streak = max(best_streak, streak)

            speed_msg = ""
            if elapsed < 2:
                speed_msg = " ⚡ lightning fast!"
            elif elapsed < 5:
                speed_msg = " nice speed!"

            console.print(
                f"  [bold green]✓ Correct![/bold green] "
                f"[dim]({elapsed:.1f}s){speed_msg}[/dim]"
            )
        else:
            streak = 0
            console.print(
                f"  [bold red]✗ Wrong.[/bold red] "
                f"Answer was [bold]{q['answer']}[/bold]  "
                f"[dim]({elapsed:.1f}s)[/dim]"
            )
        console.print()
        if qt:
            update_review_card(qt, correct)

        results.append({
            "category": q["category"],
            "question_type": qt,
            "question": q["question"],
            "correct": correct,
            "time": elapsed,
        })

    avg_time = sum(r["time"] for r in results) / len(results)
    save_session(score, num_questions, difficulty, category, avg_time)
    save_question_results(results)
    _show_summary(results, score, num_questions, best_streak)


def _show_summary(results, score, total, best_streak):
    console.rule(style="bright_magenta")
    console.print()

    pct = (score / total) * 100
    if pct == 100:
        msg = "🎯 Perfect!"
    elif pct >= 80:
        msg = "🔥 Solid run!"
    elif pct >= 60:
        msg = "👍 Not bad, keep going"
    elif pct >= 40:
        msg = "📚 Room to improve"
    else:
        msg = "💪 Keep practicing!"

    console.print(f"  [bold]{msg}[/bold]")
    console.print()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="dim")
    table.add_column(style="bold")

    table.add_row("Score", f"{score}/{total} ({pct:.0f}%)")

    avg_time = sum(r["time"] for r in results) / len(results)
    table.add_row("Avg time", f"{avg_time:.1f}s")
    table.add_row("Best streak", f"{best_streak} 🔥" if best_streak >= 2 else str(best_streak))

    # per-category breakdown
    cats = {}
    for r in results:
        cat = r["category"]
        if cat not in cats:
            cats[cat] = {"correct": 0, "total": 0}
        cats[cat]["total"] += 1
        if r["correct"]:
            cats[cat]["correct"] += 1

    for cat, data in cats.items():
        table.add_row(cat, f"{data['correct']}/{data['total']}")

    console.print(table)
    console.print()


def run_review(difficulty=1):
    console.clear()
    console.print()

    due = get_due_reviews()

    if not due:
        # try seeding from history if this is a first-time review user
        seeded = seed_review_from_history()
        if seeded:
            due = get_due_reviews()

    if not due:
        console.print(
            Panel(
                "[bold magenta]REVIEW[/bold magenta]\n"
                "[dim]nothing due for review! run a regular drill first to "
                "build up your review queue, or come back tomorrow.[/dim]",
                border_style="bright_magenta",
            )
        )
        console.print()
        return

    console.print(
        Panel(
            "[bold magenta]REVIEW MODE[/bold magenta]\n"
            f"[dim]{len(due)} question type{'s' if len(due) != 1 else ''} due for review  •  "
            f"spaced repetition (SM-2)[/dim]\n"
            f"{streak_message()}",
            border_style="bright_magenta",
        )
    )
    console.print()

    score = 0
    streak = 0
    best_streak = 0
    results = []

    for i, qt in enumerate(due, 1):
        q = question_by_type(qt, difficulty)

        console.rule(style="dim")
        header = _header(i, len(due), score, streak)
        console.print(header)
        console.print(f"\n  [bold yellow]{q['category']}[/bold yellow]  [dim](review)[/dim]")
        console.print(f"\n  {q['question']}\n")

        start = time.time()
        try:
            answer = console.input("[bold green]> [/bold green]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]quitting...[/dim]")
            return

        elapsed = time.time() - start
        correct = _check_answer(answer, q)

        if correct:
            score += 1
            streak += 1
            best_streak = max(best_streak, streak)

            speed_msg = ""
            if elapsed < 2:
                speed_msg = " ⚡ lightning fast!"
            elif elapsed < 5:
                speed_msg = " nice speed!"

            console.print(
                f"  [bold green]✓ Correct![/bold green] "
                f"[dim]({elapsed:.1f}s){speed_msg}[/dim]"
            )
        else:
            streak = 0
            console.print(
                f"  [bold red]✗ Wrong.[/bold red] "
                f"Answer was [bold]{q['answer']}[/bold]  "
                f"[dim]({elapsed:.1f}s)[/dim]"
            )
        console.print()

        update_review_card(qt, correct)
        results.append({
            "category": q["category"],
            "question_type": qt,
            "question": q["question"],
            "correct": correct,
            "time": elapsed,
        })

    avg_time = sum(r["time"] for r in results) / len(results)
    save_session(score, len(due), difficulty, "review", avg_time)
    save_question_results(results)
    _show_summary(results, score, len(due), best_streak)
