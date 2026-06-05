import telebot
from datetime import date
from src.hg_bot_tracker.classes import Habit, Completion
from src.hg_bot_tracker.habits import is_completed_today, calculate_streak
from src.database import add_habit, get_habits, add_completion, get_completions


def register(bot: telebot.TeleBot):

    @bot.message_handler(commands=["add_habit"])
    def cmd_add_habit(message):
        parts = message.text.split(maxsplit=1)

        if len(parts) < 2:
            bot.send_message(message.chat.id,
                "Укажи название привычки. Например:\n/add_habit Читать 30 минут")
            return

        name = parts[1]
        add_habit(user_id=message.from_user.id, name=name, frequency="daily")
        bot.send_message(message.chat.id, f"Привычка «{name}» добавлена! ✅")


    @bot.message_handler(commands=["habits"])
    def cmd_habits(message):
        rows = get_habits(user_id=message.from_user.id)

        if not rows:
            bot.send_message(message.chat.id, "У тебя пока нет привычек.")
            return

        text = "Твои привычки:\n\n"
        for row in rows:
            text += f"• {row['name']}\n"

        bot.send_message(message.chat.id, text)


    @bot.message_handler(commands=["done"])
    def cmd_done(message):
        parts = message.text.split(maxsplit=1)

        if len(parts) < 2:
            bot.send_message(message.chat.id,
                "Укажи название привычки. Например:\n/done Читать 30 минут")
            return

        name = parts[1]
        rows = get_habits(user_id=message.from_user.id)

        habit_row = None
        for row in rows:
            if row["name"].lower() == name.lower():
                habit_row = row
                break

        if habit_row is None:
            bot.send_message(message.chat.id, f"Привычка «{name}» не найдена.")
            return

        habit = Habit(
            id=habit_row["id"],
            name=habit_row["name"],
            frequency=habit_row["frequency"],
            created_at=date.fromisoformat(habit_row["created_at"])
        )

        completion_rows = get_completions(habit.id)
        completions = [
            Completion(
                habit_id=row["habit_id"],
                completed_at=date.fromisoformat(row["completed_at"])
            )
            for row in completion_rows
        ]

        if is_completed_today(habit, completions):
            bot.send_message(message.chat.id, f"Ты уже отметил «{name}» сегодня! 👍")
            return

        add_completion(habit.id)
        completions.append(Completion(habit_id=habit.id, completed_at=date.today()))

        streak = calculate_streak(habit, completions)
        bot.send_message(message.chat.id,f"«{name}» выполнено! ✅\n🔥 Streak: {streak} дней подряд")