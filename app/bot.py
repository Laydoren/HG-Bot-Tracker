import os
from dotenv import load_dotenv
import telebot
from src.database import init_db, add_habit, get_habits

load_dotenv()
init_db()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Привет! Я трекер привычек и целей 👋")


@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(message.chat.id,
        "/start — начать работу\n"
        "/help — список команд\n"
        "/add_habit — добавить привычку\n"
        "/habits — список привычек\n"
    )

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

bot.polling()