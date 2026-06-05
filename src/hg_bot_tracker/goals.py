from datetime import date
from src.hg_bot_tracker.classes import Goal

def get_goal_status(goal, today=None):
    if today is None:
        today = date.today()

    if goal.target is None:
        return "Done" if goal.completed else "In process"

    if goal.current >= goal.target:
        return "Done"
    elif today > goal.deadline:
        return "Not completed"
    else:
        return "In process"

def update_goal_status(goal, today=None):
    goal.status_completion = get_goal_status(goal, today)

def add_progress(goal, value):
    if goal.current + value < 0:
        raise ValueError("Progress cannot be negative")
    goal.current += value
    update_goal_status(goal)

def get_completion_percentage(goals):
    if not goals:
        return 0

    completed = sum(1 for goal in goals if goal.current >= goal.target)
    return round((completed / len(goals)) * 100, 1)

def is_overdue(goal, today=None):
    if today is None:
        today = date.today()
    if goal.completed:
        return False
    if goal.target is not None and goal.current >= goal.target:
        return False
    return today > goal.deadline

def days_remaining(goal, today=None):
    if today is None:
        today = date.today()
    left = (goal.deadline - today).days
    return left