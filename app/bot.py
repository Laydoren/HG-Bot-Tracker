import os
from dotenv import load_dotenv
import telebot
from src.database import init_db
from app.handlers import habits

load_dotenv()
init_db()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

habits.register(bot)

bot.polling()