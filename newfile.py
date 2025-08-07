
print("👀 Бот запускается...")
import requests
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

# Команда /music
@bot.message_handler(commands=['music'])
def send_music(message):
    url = "https://raw.githubusercontent.com/Petrunyandr/Petrunya_tgbot/main/zweielephanten.mp3"
    r = requests.get(url)

    if r.ok:
        with open("temp.mp3", "wb") as f:
            f.write(r.content)

        with open("temp.mp3", "rb") as audio:
            bot.send_audio(
                message.chat.id,
                audio=audio,
                caption="🎵 Вот твоя музыка!",
                title="Zwei Elephanten",
                performer="Petrunya Orchestra"
            )
    else:
        bot.send_message(message.chat.id, "❌ Ошибка при скачивании аудио.")@bot.message_handler(func=lambda message: message.text.lower() == "ку")
def ku(message):
    bot.send_message(message.chat.id, "нет")

bot.polling(none_stop=True)
