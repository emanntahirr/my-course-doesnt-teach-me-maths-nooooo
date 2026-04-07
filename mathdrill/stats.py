import json
from datetime import date, timedelta
from pathlib import Path

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
