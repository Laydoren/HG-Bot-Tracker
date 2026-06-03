from datetime import date
from src.classes import Goal

def update_goal_status(goal, today=None):
    if today is None:
        today = date.today()
    if  goal.current >= goal.target:
        goal.status_completion = "Done"
    elif today > goal.deadline:
        goal.status_completion= "Not completed"
    else:
        goal.status_completion= "In process"

