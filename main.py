import telebot
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Бот працює на Railway 🚀")

bot.infinity_polling(timeout=60, long_polling_timeout=60)
