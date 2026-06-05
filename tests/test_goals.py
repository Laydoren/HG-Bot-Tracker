from datetime import date
from src.hg_bot_tracker.classes import Goal
from src.hg_bot_tracker.goals import update_goal_status,add_progress,get_completion_percentage
import pytest

#цель выволнена
def make_goal_done():
    return Goal(
        id=1,
        title="Сделать проект",
        target=40,
        current=50,
        deadline=date(2026, 6, 10)
    )

def test_goal_done():
    goal = make_goal_done()

    update_goal_status(goal, today=date(2026, 6, 3))

    assert goal.status_completion == "Done"

#цель невыполнена
def make_goal_failed():
    return Goal(
        id=2,
        title="Сделать проект",
        target=100,
        current=30,
        deadline=date(2026, 6, 1)
    )

def test_goal_not_completed():
    goal = make_goal_failed()

    update_goal_status(goal, today=date(2026, 6, 3))

    assert goal.status_completion == "Not completed"

#Цель в процессе
def make_goal_in_progress():
    return Goal(
        id=3,
        title="Сделать проект",
        target=100,
        current=30,
        deadline=date(2026, 6, 30)
    )

def test_goal_in_process():
    goal = make_goal_in_progress()

    update_goal_status(goal, today=date(2026, 6, 3))

    assert goal.status_completion == "In process"

#Проверка на увеличение процесса
def test_add_progress_increases_current():
    goal = make_goal_in_progress()

    add_progress(goal, 10)

    assert goal.current == 40

def test_add_progress_negative_raises_error():
    goal = make_goal_in_progress()

    with pytest.raises(ValueError):
        add_progress(goal, -100)

def test_add_progress_exact_zero_allowed():
    goal = make_goal_in_progress()

    add_progress(goal, -30)

    assert goal.current == 0

#Проверка на изменение статуса
def test_add_progress_updates_status():
    goal = make_goal_in_progress()

    add_progress(goal, 70)

    assert goal.current == 100
    assert goal.status_completion == "Done"

# Все целли выполнены
def test_all_goals_completed():
    goals = [
        make_goal_done(),
        Goal(4, "test", 10, 10, date(2026, 6, 10))
    ]

    assert get_completion_percentage(goals) == 100.0

#Часть выполнена
def test_some_goals_completed():
    goals = [
        make_goal_done(),        # done
        make_goal_failed(),      # not done
        make_goal_in_progress()  # not done
    ]

    result = get_completion_percentage(goals)

    assert result == round((1 / 3) * 100, 1)

#Ни одна не выполнена
def test_no_goals_completed():
    goals = [
        make_goal_failed(),
        make_goal_in_progress()
    ]

    assert get_completion_percentage(goals) == 0.0

#Пустой список
def test_empty_goals_returns_zero():
    assert get_completion_percentage([]) == 0