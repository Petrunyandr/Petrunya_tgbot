import logging
import random
import uuid
import os

import telebot
from telebot import types
from flask import Flask, request

from config import BOT_TOKEN, VERSION
from db import Database

# --- Логирование ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

bot = telebot.TeleBot(BOT_TOKEN)
db = Database()
app = Flask(__name__)

temp_photos = {}  # временное хранилище для подтверждения фото

# --- Команды ---
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id, "Привет! Отправь фото, чтобы сохранить его в базу данных 🖼️"
    )

@bot.message_handler(commands=["list"])
def list_photos(message):
    try:
        photos = db.get_photos()
        if not photos:
            bot.send_message(message.chat.id, "В базе пока нет фото 😢")
            return

        text = "🖼️ Список фото:\n\n"
        for i, p in enumerate(photos, 1):
            text += f"{i}. {p['file_id']} — {p['username']} ({p['date'][:16]})\n"

        bot.send_message(message.chat.id, text)
    except Exception as e:
        logging.error(f"Ошибка при получении списка фото: {e}")
        bot.send_message(message.chat.id, "Ошибка при получении списка фото.")

@bot.message_handler(commands=["photo"])
def send_random_photo(message):
    photos = db.get_photos()
    if not photos:
        bot.send_message(message.chat.id, "В базе пока нет фото 😢")
        return
    chosen = random.choice(photos)
    bot.send_photo(
        chat_id=message.chat.id,
        photo=chosen["file_id"],
        caption=f"От {chosen['username']} ({chosen['date'][:16]})",
    )

# --- Получение фото и подтверждение ---
@bot.message_handler(content_types=["photo"])
def confirm_photo(message):
    photo = message.photo[-1]  # самое большое фото
    file_id = photo.file_id

    if db.photo_exists(file_id):
        bot.send_message(message.chat.id, "Это фото уже сохранено в базе!")
        return

    short_id = str(uuid.uuid4())
    temp_photos[short_id] = {
        "file_id": file_id,
        "username": message.from_user.username or "Unknown",
        "caption": message.caption or "",
    }

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Сохранить", callback_data=f"save_{short_id}"),
        types.InlineKeyboardButton("❌ Отмена", callback_data=f"cancel_{short_id}"),
    )

    bot.send_message(
        message.chat.id,
        f"Вы хотите сохранить это фото в базу?\n\n{message.caption or ''}",
        reply_markup=markup,
    )

# --- Callback кнопки ---
@bot.callback_query_handler(func=lambda call: call.data.startswith(("save_", "cancel_")))
def handle_callback(call):
    action, short_id = call.data.split("_", 1)
    if short_id not in temp_photos:
        bot.answer_callback_query(call.id, "Срок действия кнопки истек")
        return

    data = temp_photos.pop(short_id)
    file_id = data["file_id"]
    username = data["username"]

    if action == "save":
        try:
            db.add_photo(file_id, "", username)
            bot.edit_message_text(
                "Фото успешно сохранено ✅",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            logging.error(f"Ошибка при сохранении фото: {e}")
            bot.edit_message_text(
                "Не удалось сохранить фото :(",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
    else:
        bot.edit_message_text(
            "Сохранение фото отменено ❌",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )

# --- Вебхук ---
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "ok", 200
    else:
        return "unsupported", 403

# --- Установка вебхука при запуске ---
def setup_webhook():
    RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if not RENDER_HOSTNAME:
        logging.error("Нет RENDER_EXTERNAL_HOSTNAME!")
        return

    WEBHOOK_URL = f"https://{RENDER_HOSTNAME}/webhook"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")

# --- Запуск Flask ---
if __name__ == "__main__":
    setup_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))