import logging
import random
import uuid

import telebot as t
from telebot import types

from config import BOT_TOKEN, VERSION
from db import Database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


class Bot:
    def __init__(self):
        self.bot = t.TeleBot(BOT_TOKEN)
        self.db = Database()
        self.temp_photos = {}  # Для временного хранения фото перед подтверждением
        self.setup_commands()
        self.setup_callbacks()

    def setup_commands(self):
        self.bot.set_my_commands(
            [
                types.BotCommand("start", "начать работу 😁"),
                types.BotCommand("list", "список фото 🖼️"),
                types.BotCommand("photo", "случайное фото 🎲"),
            ]
        )

        self.bot.message_handler(commands=["start"])(self.start)
        self.bot.message_handler(commands=["list"])(self.list_photos)
        self.bot.message_handler(commands=["photo"])(self.send_random_photo)
        self.bot.message_handler(content_types=["photo"])(self.confirm_photo)


    def start(self, message):
        self.bot.send_message(
            message.chat.id, "Привет! Отправь фото, чтобы сохранить его в базу данных 🖼️"
        )

    def confirm_photo(self, message):
        photo = message.photo[-1]  # самое большое фото
        file_id = photo.file_id

        if self.db.photo_exists(file_id):
            self.bot.send_message(message.chat.id, "Это фото уже сохранено в базе!")
            return

        # Создаем уникальный короткий ID для кнопки
        short_id = str(uuid.uuid4())
        self.temp_photos[short_id] = {
            "file_id": file_id,
            "username": message.from_user.username or "Unknown",
            "caption": message.caption or "",
        }

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "✅ Сохранить", callback_data=f"save_{short_id}"
            ),
            types.InlineKeyboardButton("❌ Отмена", callback_data=f"cancel_{short_id}"),
        )

        self.bot.send_message(
            message.chat.id,
            f"Вы хотите сохранить это фото в базу?\n\n{message.caption or ''}",
            reply_markup=markup,
        )

    def send_random_photo(self, message):
        photos = self.db.get_photos()
        if not photos:
            self.bot.send_message(message.chat.id, "В базе пока нет фото 😢")
            return
        chosen = random.choice(photos)
        self.bot.send_photo(
            chat_id=message.chat.id,
            photo=chosen["file_id"],
            caption=f"От {chosen['username']} ({chosen['date'][:16]})",
        )

    def setup_callbacks(self):
        @self.bot.callback_query_handler(
            func=lambda call: call.data.startswith(("save_", "cancel_"))
        )
        def handle_callback(call):
            action, short_id = call.data.split("_", 1)
            if short_id not in self.temp_photos:
                self.bot.answer_callback_query(call.id, "Срок действия кнопки истек")
                return

            data = self.temp_photos.pop(short_id)
            file_id = data["file_id"]
            username = data["username"]

            if action == "save":
                try:
                    self.db.add_photo(file_id, "", username)
                    self.bot.edit_message_text(
                        "Фото успешно сохранено ✅",
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                    )
                except Exception as e:
                    logging.error(f"Ошибка при сохранении фото: {e}")
                    self.bot.edit_message_text(
                        "Не удалось сохранить фото :(",
                        chat_id=call.message.chat.id,
                        message_id=call.message.message_id,
                    )
            else:
                self.bot.edit_message_text(
                    "Сохранение фото отменено ❌",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                )

    def list_photos(self, message):
        try:
            photos = self.db.get_photos()
            if not photos:
                self.bot.send_message(message.chat.id, "В базе пока нет фото 😢")
                return

            text = "🖼️ Список фото:\n\n"
            for i, p in enumerate(photos, 1):
                text += f"{i}. {p['file_id']} — {p['username']} ({p['date'][:16]})\n"

            self.bot.send_message(message.chat.id, text)
        except Exception as e:
            logging.error(f"Ошибка при получении списка фото: {e}")
            self.bot.send_message(message.chat.id, "Ошибка при получении списка фото.")

    def run(self):
        print("🚀 Бот запущен (polling)")
        try:
            self.bot.delete_webhook()
        except Exception as e:
            print(f"Не удалось удалить вебхук: {e}")
        try:
            self.bot.send_message(
                -1002515025726, f"Бот запущен и готов к работе! Версия {VERSION}"
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение: {e}")
        self.bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    Bot().run()
