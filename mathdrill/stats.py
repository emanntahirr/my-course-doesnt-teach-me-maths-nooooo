import json
from datetime import date, timedelta
from pathlib import Path

from rich.console import Console
from rich.table import Table

DATA_DIR = Path.home() / ".mathdrill"
HISTORY_FILE = DATA_DIR / "history.json"


def _ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)


def load_history():
    if not HISTORY_FILE.exists():
        return {"sessions": []}
    with open(HISTORY_FILE) as f:
        return json.load(f)


def save_session(score, total, difficulty, category, avg_time):
    _ensure_data_dir()
    history = load_history()
    history["sessions"].append({
        "date": date.today().isoformat(),
        "score": score,
        "total": total,
        "difficulty": difficulty,
        "category": category,
        "avg_time": round(avg_time, 1),
    })
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def save_question_results(question_results):
    _ensure_data_dir()
    history = load_history()
    if "questions" not in history:
        history["questions"] = []
    for r in question_results:
        entry = {
            "date": date.today().isoformat(),
            "category": r["category"],
            "correct": r["correct"],
        }
        if "question_type" in r:
            entry["question_type"] = r["question_type"]
        history["questions"].append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def get_weak_categories():
    history = load_history()
    questions = history.get("questions", [])
    if not questions:
        return None

    cats = {}
    for q in questions:
        cat = q["category"]
        if cat not in cats:
            cats[cat] = {"correct": 0, "total": 0}
        cats[cat]["total"] += 1
        if q["correct"]:
            cats[cat]["correct"] += 1

    scored = []
    for cat, data in cats.items():
        pct = data["correct"] / data["total"] if data["total"] else 1
        scored.append((cat, pct))

    scored.sort(key=lambda x: x[1])

    if not scored or scored[0][1] >= 0.8:
        return None

    weak = [cat for cat, pct in scored if pct < 0.8]
    return weak if weak else None


def get_streak():
    history = load_history()
    if not history["sessions"]:
        return 0

    practice_dates = {s["date"] for s in history["sessions"]}
    today = date.today()
    streak = 0

    # check today first, then go backwards
    day = today
    while day.isoformat() in practice_dates:
        streak += 1
        day -= timedelta(days=1)

    # if the user hasn't practiced today yet, check streak
    # ending yesterday so we can still show their active streak
    if streak == 0:
        day = today - timedelta(days=1)
        while day.isoformat() in practice_dates:
            streak += 1
            day -= timedelta(days=1)

    return streak


def practiced_today():
    history = load_history()
    today = date.today().isoformat()
    return any(s["date"] == today for s in history["sessions"])


def streak_message():
    streak = get_streak()
    today_done = practiced_today()

    if streak == 0:
        return "First session! Start your streak today."

    if today_done:
        if streak >= 30:
            return f"🔥 {streak}-day streak! Unstoppable!"
        elif streak >= 7:
            return f"🔥 {streak}-day streak! On fire!"
        elif streak >= 3:
            return f"🔥 {streak}-day streak! Keep it up!"
        else:
            return f"🔥 {streak}-day streak!"
    else:
        if streak >= 7:
            return f"⚠️  {streak}-day streak — practice today to keep it alive!"
        elif streak >= 1:
            return f"{streak}-day streak — don't break the chain!"
        return "First session! Start your streak today."


# ── spaced repetition (SM-2) ────────────────────────────────────────

REVIEW_FILE = DATA_DIR / "review.json"


def _load_review_cards():
    if not REVIEW_FILE.exists():
        return {}
    with open(REVIEW_FILE) as f:
        return json.load(f)


def _save_review_cards(cards):
    _ensure_data_dir()
    with open(REVIEW_FILE, "w") as f:
        json.dump(cards, f, indent=2)


def update_review_card(question_type, correct):
    """Update SM-2 data for a question type after answering it."""
    cards = _load_review_cards()
    today = date.today().isoformat()

    if question_type not in cards:
        cards[question_type] = {
            "ef": 2.5,
            "interval": 1,
            "repetitions": 0,
            "next_review": today,
        }

    card = cards[question_type]

    # SM-2: quality 4 for correct, 1 for wrong
    q = 4 if correct else 1
    card["ef"] = max(1.3, card["ef"] + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))

    if correct:
        card["repetitions"] += 1
        if card["repetitions"] == 1:
            card["interval"] = 1
        elif card["repetitions"] == 2:
            card["interval"] = 3
        else:
            card["interval"] = round(card["interval"] * card["ef"])
    else:
        card["repetitions"] = 0
        card["interval"] = 1

    next_date = date.today() + timedelta(days=card["interval"])
    card["next_review"] = next_date.isoformat()

    cards[question_type] = card
    _save_review_cards(cards)


def get_due_reviews():
    """Return list of question_types that are due for review today or earlier."""
    cards = _load_review_cards()
    today = date.today().isoformat()
    due = [qt for qt, card in cards.items() if card["next_review"] <= today]
    # sort by next_review (oldest first) then by easiness (hardest first)
    due.sort(key=lambda qt: (cards[qt]["next_review"], cards[qt]["ef"]))
    return due


def seed_review_from_history():
    """Create review cards from existing question history for users who already have data."""
    history = load_history()
    questions = history.get("questions", [])
    if not questions:
        return 0

    cards = _load_review_cards()
    seeded = 0
    # group by question_type if present, otherwise by category
    type_stats = {}
    for q in questions:
        qt = q.get("question_type")
        if not qt:
            continue
        if qt not in type_stats:
            type_stats[qt] = {"correct": 0, "total": 0}
        type_stats[qt]["total"] += 1
        if q["correct"]:
            type_stats[qt]["correct"] += 1

    today = date.today().isoformat()
    for qt, data in type_stats.items():
        if qt not in cards:
            pct = data["correct"] / data["total"] if data["total"] else 0.5
            cards[qt] = {
                "ef": max(1.3, 1.3 + pct * 1.2),
                "interval": 1,
                "repetitions": 0,
                "next_review": today,
            }
            seeded += 1

    if seeded:
        _save_review_cards(cards)
    return seeded


def show_stats():
    console = Console()
    history = load_history()
    sessions = history["sessions"]

    if not sessions:
        console.print("\nno sessions yet. run a drill first!\n")
        return

    streak = get_streak()
    total_sessions = len(sessions)
    total_questions = sum(s["total"] for s in sessions)
    total_correct = sum(s["score"] for s in sessions)
    overall_pct = (total_correct / total_questions) * 100 if total_questions else 0
    avg_time = sum(s["avg_time"] for s in sessions) / total_sessions

    console.print()
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="dim")
    table.add_column(style="bold")

    table.add_row("current streak", f"{streak} days")
    table.add_row("total sessions", str(total_sessions))
    table.add_row("total questions", str(total_questions))
    table.add_row("overall accuracy", f"{total_correct}/{total_questions} ({overall_pct:.0f}%)")
    table.add_row("avg time", f"{avg_time:.1f}s")

    # per-category breakdown
    cats = {}
    for s in sessions:
        cat = s.get("category") or "mixed"
        if cat not in cats:
            cats[cat] = {"score": 0, "total": 0}
        cats[cat]["score"] += s["score"]
        cats[cat]["total"] += s["total"]

    console.print(table)
    console.print()

    if len(cats) > 1 or "mixed" not in cats:
        cat_table = Table(title="by category", box=None, padding=(0, 2))
        cat_table.add_column("category", style="dim")
        cat_table.add_column("score", style="bold")

        for cat, data in sorted(cats.items()):
            pct = (data["score"] / data["total"]) * 100 if data["total"] else 0
            cat_table.add_row(cat, f"{data['score']}/{data['total']} ({pct:.0f}%)")

        console.print(cat_table)
        console.print()
