from datetime import date
from src.classes import Habit, Completion
from src.habits import is_completed_today

def make_habit(id=1):
    return Habit(id=id, name="Кодить для души", frequency="daily", created_at=date(2026, 6, 3))

def test_completed_today_true():
    habit = make_habit()
    completions = [Completion(habit_id=1, completed_at=date(2026, 6, 3))]

    result = is_completed_today(habit, completions, date(2026, 6, 3))

    assert result is True

def test_completed_today_false():
    habit = make_habit()
    completions = [Completion(habit_id=1, completed_at=date(2026, 6, 3))]

    result = is_completed_today(habit, completions, today=date(2000, 1, 1))

    assert result is False