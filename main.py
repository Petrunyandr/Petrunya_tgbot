import logging
import random

import telebot as t
from telebot import types

from db import Database
from config import *

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
        self.setup_commands()

    def setup_commands(self):
        self.bot.set_my_commands(
            [
                types.BotCommand("start", "начать работу 😁"),
                types.BotCommand("music", "послушать музыку 🎵"),
                types.BotCommand("list", "список треков 📜"),
            ]
        )

        self.bot.message_handler(commands=["start"])(self.start)
        self.bot.message_handler(commands=["music"])(self.send_random_music)
        self.bot.message_handler(commands=["list"])(self.list_tracks)
        self.bot.message_handler(content_types=["audio", "voice"])(self.get_file_id)

        self.bot.message_handler(
            func=lambda m: m.text.lower() in ("пр", "ку", "qq", "pr", "qu", "ku")
        )(self.ku)
        self.bot.message_handler(
            func=lambda m: m.text.lower() in ("спс", "спасибо", "о спс")
        )(self.sps)
        self.bot.message_handler(
            func=lambda m: m.text.lower()
            in ("ебало", "вальни ебало", "завали ебало", "ебло")
        )(self.ebalo)
        self.bot.message_handler(
            func=lambda m: m.text.lower()
            in (
                "иди нахуй",
                "иди нахуц",
                "иди назуй",
                "иди в пизду",
                "иди в пиздц",
                "нахуй иди",
                "назуй иди",
            )
        )(self.mneme)
        self.bot.message_handler(func=lambda m: m.text.lower() in ["сори", "сорян", "прости"])(
            self.jdnd
        )
        self.bot.message_handler(func=lambda m: m.text.lower() == "але")(self.ale)

    def start(self, message):
        self.bot.send_message(
            message.chat.id, "Привет! Напиши /music, чтобы послушать музыку 🎧"
        )

    def get_file_id(self, message):
        audio = message.audio or message.voice
        if not audio:
            return

        if message.audio:
            title = audio.title or "Без названия"
            performer = audio.performer or "Неизвестный исполнитель"
        else:
            title = "Голосовое сообщение"
            performer = "Неизвестный"
        if not self.db.track_exists(audio.file_id):
            try:
                self.db.add_track(audio.file_id, title, performer, audio.duration)
                logging.info(f"Сохранен трек {title} - {performer}")
                self.bot.send_message(message.chat.id, f"Трек сохранён в базу данных!")
            except Exception as e:
                logging.error(f"Ошибка при сохранении трека: {e}")
                self.bot.send_message(message.chat.id, "Не удалось сохранить трек :(")
        else:
            self.bot.send_message(message.chat.id, "Файл уже сохранен")

    def list_tracks(self, message):
        try:
            tracks = self.db.get_tracks()
            if not tracks:
                self.bot.send_message(message.chat.id, "В коллекции пока нет треков 😢")
                return

            text = "🎵 Список треков:\n\n"
            for i, tr in enumerate(tracks, 1):
                text += f"{i}. {tr['title']} — {tr['performer']}\n"

            self.bot.send_message(message.chat.id, text)
        except Exception as e:
            logging.error(f"Ошибка при получении списка треков: {e}")
            self.bot.send_message(
                message.chat.id, "Ошибка при получении списка треков."
            )

    def send_random_music(self, message):
        try:
            tracks = self.db.get_tracks()
            if not tracks:
                self.bot.send_message(message.chat.id, "В коллекции пока нет треков 😢")
                return

            chosen_track = random.choice(tracks)
            self.bot.send_audio(
                chat_id=message.chat.id,
                audio=chosen_track["track_id"],
                title=chosen_track["title"],
                performer=chosen_track["performer"],
                duration=chosen_track["duration"],
                caption="лутай",
            )
        except Exception as e:
            logging.error(f"Ошибка при отправке музыки: {e}")
            self.bot.send_message(message.chat.id, "Ошибка при отправке музыки.")

    def ku(self, message):
        self.bot.send_message(message.chat.id, "ООООО ПР")

    def sps(self, message):
        self.bot.send_message(message.chat.id, "нез")

    def ebalo(self, message):
        self.bot.send_message(message.chat.id, "сам")

    def mneme(self, message):
        self.bot.send_message(message.chat.id, "не буду🤣🤣🤣")

    def jdnd(self, message):
        self.bot.send_message(message.chat.id, "прощон")

    def ale(self, message):
        self.bot.send_message(message.chat.id, "туда")
    
    def shaverma(self, message):
        self.bot.send_message(message.chat.id, "ЛЕЕЕЕЕ БРАТКА ДЕРЖИ")

    def run(self):
        print("🚀 Бот запущен (polling)")
        try:
            self.bot.send_message(-1002515025726, f"Бот запущен и готов к работе! Версия {VERSION}")
        except Exception as e:
            print(f"Не удалось отправить сообщение: {e}")
        self.bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    Bot().run()
