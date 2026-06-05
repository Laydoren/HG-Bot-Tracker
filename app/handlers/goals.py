import telebot
from datetime import date
from src.hg_bot_tracker.classes import Goal
from src.hg_bot_tracker.goals import add_progress, update_goal_status, days_remaining, is_overdue
from src.database import add_goal, get_goals, update_goal_progress, update_goal_completed

def register(bot: telebot.TeleBot):

    @bot.message_handler(commands=["add_goal"])
    def cmd_add_goal(message):
        parts = message.text.split(maxsplit=1)

        if len(parts) < 2:
            bot.send_message(message.chat.id,
                "Укажи название цели. Например:\n"
                "/add_goal Прочитать 12 книг; 12; 2026-12-31\n"
                "или без target:\n"
                "/add_goal Сходить на концерт; 2026-12-31")
            return

        arg = parts[1].split(";")
        arg = [a.strip() for a in arg]

        try:
            if len(arg) == 3:
                title, target, deadline = arg
            elif len(arg) == 2:
                title, deadline = arg
                target = None
            else:
                raise ValueError

            deadline_date = date.fromisoformat(deadline)

        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат. Попробуй ещё раз")
            return

        add_goal(user_id=message.from_user.id, title=title, deadline=deadline, target=target)
        bot.send_message(message.chat.id, f"Цель «{title}» добавлена")


    @bot.message_handler(commands=["goals"])
    def cmd_goals(message):
        rows = get_goals(user_id=message.from_user.id)

        if not rows:
            bot.send_message(message.chat.id, "У тебя пока нет целей")
            return

        text = "Твои цели:\n\n"
        for row in rows:
            goal = Goal(id=row["id"], title=row["title"], target=row["target"], current=row["current"], deadline=date.fromisoformat(row["deadline"]), completed=bool(row["completed"]))

            update_goal_status(goal)

            overdue = is_overdue(goal)
            days = days_remaining(goal)

            if goal.target is not None:
                text += f"* {goal.title} - {goal.current}/{goal.target}"
            else:
                text += f"* {goal.title}"

            text += f" [{goal.status_completion}]"

            if days >= 0:
                text += f" - осталось {days} дн.\n"
            else:
                text += f" - просрочено на {abs(days)} дн.\n"

        bot.send_message(message.chat.id, text)


    @bot.message_handler(commands=["progress"])
    def cmd_progress(message):
        parts = message.text.split(maxsplit=1)

        if len(parts) < 2:
            bot.send_message(message.chat.id,
                             "Укажи название цели и значение\n Например:\n"
                             "/progress Прочитать 12 книг; 3")
            return

        args = parts[1].split(";")
        args = [a.strip() for a in args]

        if len(args) != 2:
            bot.send_message(message.chat.id, "Неверный формат. Попробуй ещё раз")
            return

        title, value = args
        try:
            value = float(value)
        except ValueError:
            bot.send_message(message.chat.id, "Значение должно быть числом")
            return

        rows = get_goals(user_id=message.from_user.id)

        goal_row = None
        for row in rows:
            if row["title"].lower() == title.lower():
                goal_row = row
                break

        if goal_row is None:
            bot.send_message(message.chat.id, f"Цель «{title}» не найдена")
            return

        goal = Goal(id=goal_row["id"], title=goal_row["title"], target=goal_row["target"], current=goal_row["current"], deadline=date.fromisoformat(goal_row["deadline"]), completed=bool(goal_row["completed"]))

        if goal.target is None:
            if value not in (0, 1):
                bot.send_message(message.chat.id, "Для этой цели укажи 1 (выполнено) или 0 (не выполнено)")
                return

            goal.completed = bool(value)
            update_goal_completed(goal.id, goal.completed)
            status = "выполнена" if goal.completed else "сброшена"
            bot.send_message(message.chat.id, f"Цель «{goal.title}» {status}")
        else:
            try:
                add_progress(goal, value)
            except ValueError as e:
                bot.send_message(message.chat.id, str(e))
                return

            update_goal_progress(goal.id, goal.current)
            bot.send_message(message.chat.id, f"Прогресс обновлён «{goal.title}» - {goal.current}/{goal.target} [{goal.status_completion}]")
