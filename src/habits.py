from datetime import date
from src.classes import Habit, Completion

def is_completed_today(habit, completions, today = None):
    if today is None:
        today = date.today()

    for completion in completions:
        if completion.habit_id == habit.id and completion.completed_at == today:
            return True

    return False


# habit = Habit(id=1, name="Reading", frequency="daily", created_at=date(2024, 1, 1))
#
# completions = [
#     Completion(habit_id=1, completed_at=date(2024, 6, 10)),
#     Completion(habit_id=1, completed_at=date(2024, 6, 11)),
# ]
#
# print(is_completed_today(habit, completions, today=date(2024, 6, 11)))
# print(is_completed_today(habit, completions, today=date(2024, 6, 12)))