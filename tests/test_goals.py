from datetime import date
from src.classes import Goal
from src.goals import update_goal_status,add_progress
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