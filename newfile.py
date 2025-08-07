print("👀 Бот запускается...")

import os
from dotenv import load_dotenv
import telebot as t
from telebot import types

print("✅ Импорт выполнен")

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN не найден в переменных окружения")

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

@bot.message_handler(commands=['music'])
def send_music(message):
    audio_url = (
        "https://raw.githubusercontent.com/"
        "Petrunyandr/Petrunya_tgbot/main/zweielephanten.mp3"
    )
    bot.send_audio(
        chat_id=message.chat.id,
        audio=audio_url,
        caption="нез",
        title="Zwei Elephanten",         
        performer="Наталия Владимировна"   
    )
@bot.message_handler(func=lambda message: message.text.lower() == "ку")
def ku(message):
    bot.send_message(message.chat.id, "нет")

# Запуск бота
bot.polling(none_stop=True)
