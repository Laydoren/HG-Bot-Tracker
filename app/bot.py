import os
from dotenv import load_dotenv
import telebot
from src.database import init_db
from app.handlers import habits, goals

load_dotenv()
init_db()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

habits.register(bot)

goals.register(bot)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Привет! Я трекер привычек и целей 👋\n""Для просмотра команд пропишите /start")


@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(message.chat.id,
        "/start — начать работу\n"
        "/help — список команд\n"
        "/add_habit — добавить привычку\n"
        "/habits — список привычек\n"
        "/done — отметить выполнение\n"
        "/add_goal — добавить цель\n"
        "/goals — список целей\n"
        "/progress — добавить прогресс цели\n"
    )


if __name__ == "__main__":
    bot.polling()