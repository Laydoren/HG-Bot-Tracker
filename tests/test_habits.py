from datetime import date
from src.classes import Habit, Completion
from src.habits import is_completed_today, calculate_streak


def make_habit(id=1):
    return Habit(id=id, name="Кодить для души", frequency="daily", created_at=date(2026, 6, 3))


# is_completed_today tests

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

def test_empty_completions_returns_false():
    habit = make_habit()

    result = is_completed_today(habit, [], today=date(2000, 1, 1))

    assert result is False

def test_completion_for_different_habits_false():
    habit = make_habit(id=2)
    completions = [Completion(habit_id=3, completed_at=date(2024, 6, 11))]

    result = is_completed_today(habit, completions, today=date(2024, 6, 11))

    assert result is False


# calculate_streak tests

def test_streak_of_some_days():
    habit = make_habit()
    completions = [
        Completion(habit_id=1, completed_at=date(2026, 6, 1)),
        Completion(habit_id=1, completed_at=date(2026, 6, 2)),
        Completion(habit_id=1, completed_at=date(2026, 6, 3)),
    ]

    result = calculate_streak(habit, completions, today=date(2026, 6, 3))

    assert result == 3

def test_streak_breaks_on_missing_day():
    habit = make_habit()
    completions = [
        Completion(habit_id=1, completed_at=date(2026, 6, 1)),
        Completion(habit_id=1, completed_at=date(2026, 6, 2)),
        Completion(habit_id=1, completed_at=date(2026, 6, 4)),
        Completion(habit_id=1, completed_at=date(2026, 6, 5))
    ]

    result = calculate_streak(habit, completions, today=date(2026, 6, 5))

    assert result == 2

def test_streak_zero_if_missed_today():
    habit = make_habit()
    completions = [
        Completion(habit_id=1, completed_at=date(2024, 6, 1)),
        Completion(habit_id=1, completed_at=date(2024, 6, 2)),
    ]

    result = calculate_streak(habit, completions, today=date(2024, 6, 3))

    assert result == 0

def test_streak_zero_for_empty_completions():
    habit = make_habit()

    result = calculate_streak(habit, [], today=date(2026, 6, 3))

    assert result == 0

def test_streak_ignores_other_habits():
    habit = make_habit(id=2)
    completions = [
        Completion(habit_id=3, completed_at=date(2026, 6, 1)),
        Completion(habit_id=3, completed_at=date(2026, 6, 2)),
        Completion(habit_id=3, completed_at=date(2026, 6, 3))
    ]

    result = calculate_streak(habit, completions, today=date(2026, 6, 3))

    assert result == 0