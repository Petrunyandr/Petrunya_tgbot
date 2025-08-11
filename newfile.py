print("👀 Бот запускается...")

import os
from dotenv import load_dotenv
import telebot as t
from telebot import types
from flask import Flask, request

print("✅ Импорт выполнен")

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL") 

bot = t.TeleBot(BOT_TOKEN)
server = Flask(__name__)

bot.set_my_commands([
    types.BotCommand("start", "начать работу 😁"),
    types.BotCommand("music", "послушать музыку 🎵")
])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши /music, чтобы послушать музыку 🎧")


@bot.message_handler(commands=['music'])
def send_music(message):
    bot.send_audio(
        chat_id=message.chat.id,
        audio="CQACAgIAAxkBAAE5Vd1omdUEdweQlxY-fQkrrkNmjqV7hgACUW0AAklmAAFL-wKswKyHlAY2BA",  
        title="Zwei elefanten",
        performer="Наталия Владимировна",
        duration=97, 
        thumb="AgACAgIAAxkBAAE5VtJomedGl-yTo_nWnBKnI5xYZKa6rQACwvIxG0XU0EjhdZOl1E3voAEAAwIAA3MAAzYE",
        caption="лутай"
    )

@bot.message_handler(func=lambda message: message.text.lower() == "ку")
def ku(message):
    bot.send_message(message.chat.id, "нет")

@bot.message_handler(func=lambda message: message.text.lower() == "пр")
def pr(message):
    bot.send_message(message.chat.id, "Сори")

@bot.message_handler(func=lambda message: message.text.lower() == "ебало")
def ebalo(message):
    bot.send_message(message.chat.id, "сам")

@server.route("/", methods=['GET'])
def home():
    return "Бот работает 👌"

@server.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = t.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{APP_URL}/{BOT_TOKEN}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{APP_URL}/{BOT_TOKEN}")
    server.run(host="0.0.0.0",
port=int(os.environ.get("PORT", 5000)))
