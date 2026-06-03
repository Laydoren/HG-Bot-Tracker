import os
from dotenv import load_dotenv
import telebot
from src.database import init_db

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
    )


bot.polling()