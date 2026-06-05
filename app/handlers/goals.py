import telebot
from datetime import date
from src.hg_bot_tracker.classes import Goal
from src.hg_bot_tracker.goals import add_progress, update_goal_status, days_remaining, is_overdue
from src.database import add_goal, get_goals, update_goal_progress

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