from datetime import date

class Habit:
    def __init__(self, id, name, frequency, created_at):
        self.id = id
        self.name = name
        self.frequency = frequency
        self.created_at = created_at

    def __repr__(self):
        return f'({self.id}, {self.name}, {self.frequency}, {self.created_at})'


class Completion:
    def __init__(self, habit_id, completed_at):
        self.habit_id = habit_id
        self.completed_at = completed_at

    def __repr__(self):
        return f'({self.habit_id}, {self.completed_at})'


class Goal:
    def __init__(self, id, title, target, current, deadline):
        self.id = id
        self.title = title
        self.target = target
        self.current = current
        self.deadline = deadline

    def __repr__(self):
        return f'({self.id}, {self.title}, {self.target}, {self.deadline})'



