from datetime import date, timedelta
from hg_bot_tracker.classes import Habit, Completion

def is_completed_today(habit, completions, today = None):
    if today is None:
        today = date.today()

    for completion in completions:
        if completion.habit_id == habit.id and completion.completed_at == today:
            return True

    return False


def calculate_streak(habit, completions, today=None):
    if today is None:
        today = date.today()

    completed_dates = set(c.completed_at for c in completions if c.habit_id == habit.id)

    streak = 0
    current_day = today

    while current_day in completed_dates:
        streak += 1
        current_day = current_day - timedelta(days=1)

    return streak

