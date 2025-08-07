import os
from dotenv import load_dotenv
import telebot as t
from telebot import types

# Загружаем окруж.
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = t.TeleBot(BOT_TOKEN)

# Устанавливаем команды
bot.set_my_commands([
    types.BotCommand("start", "начать работу 😁"),
    types.BotCommand("music", "послушать музыку 🎵")
])

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши /music, чтобы послушать музыку 🎧")

# Команда /music
@bot.message_handler(commands=['music'])
def music(message):
    audio_url = "https://github.com/Petrunyandr/Petrunya_tgbot/blob/main/zweielephanten.mp3"  # замени на свою ссылку
    bot.send_audio(message.chat.id, audio=audio_url, caption="Вот твоя музыка 🎶")
@bot.message_handler(func=lambda message: message.text.lower() == "ку")
def ku(message):
    bot.send_message(message.chat.id, "нет")

# Запуск бота
bot.polling(none_stop=True)
