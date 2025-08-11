print("👀 Бот запускается...")

import os
from dotenv import load_dotenv
import telebot as t
from telebot import types
from flask import Flask, request

print("✅ Импорт выполнен")

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # например, https://mybot.onrender.com

if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN не найден в переменных окружения")

if not APP_URL:
    raise Exception("❌ APP_URL не найден (укажи URL Render сервиса в переменных окружения)")

bot = t.TeleBot(BOT_TOKEN)
server = Flask(__name__)

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
    audio_url = "https://github.com/Petrunyandr/Petrunya_tgbot/raw/main/zweielephanten.mp3"
    bot.send_audio(message.chat.id, audio=audio_url, caption="Вот твоя музыка 🎶")

@bot.message_handler(func=lambda message: message.text.lower() == "ку")
def ku(message):
    bot.send_message(message.chat.id, "нет")

# Flask route для проверки
@server.route("/", methods=['GET'])
def home():
    return "Бот работает 👌"

# Flask route для Telegram webhook
@server.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = t.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# Установка webhook
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{APP_URL}/{BOT_TOKEN}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{APP_URL}/{BOT_TOKEN}")
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
