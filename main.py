import logging
import os
import random
import telebot as t
from dotenv import load_dotenv
from telebot import types


load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = t.TeleBot(BOT_TOKEN)

bot.set_my_commands(
    [
        types.BotCommand("start", "начать работу 😁"),
        types.BotCommand("music", "послушать музыку 🎵"),
    ]
)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id, "Привет! Напиши /music, чтобы послушать музыку 🎧"
    )


track1 = {
    "file_id": "CQACAgIAAxkBAAE5Vd1omdUEdweQlxY-fQkrrkNmjqV7hgACUW0AAklmAAFL-wKswKyHlAY2BA",
    "title": "Zwei elefanten",
    "performer": "Наталия Владимировна",
    "duration": 97,
}
track2 = {
    "file_id": "CQACAgIAAyEFAASV6D8-AAIF-WiaPbD10kdILCq1F8QlxKT-EHMwAAI4hwAC17LQSClF2JMqiy5bNgQ",
    "title": "СКОРАЙШЕГО ВЫЗДОРОВЛЕНИЯ",
    "performer": "ГАПОРД",
    "duration": 182,
}

track3 = {
    "file_id": "CQACAgIAAxkBAAE5XANomjbLqBFMyrD2rl51Aw1ToPe4EwACVm8AApsyeUgiDrL8jRWk1TYE",
    "title": "Stayin' alive",
    "performer": "Bee Gees",
    "duration": 287,
}


@bot.message_handler(content_types=["audio", "voice"])
def get_file_id(message):
    audio = message.audio or message.voice
    if audio:
        logging.info(f"Получен file_id: {audio.file_id} от {message.from_user.id}")
        bot.send_message(message.chat.id, f"file_id для этого аудио:\n{audio.file_id}")


@bot.message_handler(commands=["music"])
def send_random_music(message):
    logging.info(f"/music от {message.from_user.id} @{message.from_user.username}")
    chosen_track = random.choice([track1, track2, track3])
    try:
        bot.send_audio(
            chat_id=message.chat.id,
            audio=chosen_track["file_id"],
            title=chosen_track["title"],
            performer=chosen_track["performer"],
            duration=chosen_track["duration"],
            caption="лутай",
        )
        logging.info(
            f"Отправлена музыка '{chosen_track['title']}' пользователю {message.from_user.id}"
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке музыки: {e}")


@bot.message_handler(func=lambda message: message.text.lower() == "ку")
def ku(message):
    bot.send_message(message.chat.id, "нет")

@bot.message_handler(
    func=lambda message: message.text.lower() in ("спс", "спасибо", "о спс")
)
def sps(message):
    bot.send_message(message.chat.id, "нез")


@bot.message_handler(func=lambda message: message.text.lower() == "пр")
def pr(message):
    bot.send_message(message.chat.id, "пр")


@bot.message_handler(func=lambda message: message.text.lower() == "ебало")
def ebalo(message):
    bot.send_message(message.chat.id, "сам")


@bot.message_handler(
    func=lambda message: message.text.lower()
    in ("иди нахуй", "иди нахуц", "иди назуй", "иди в пизду", "иди в пиздц")
)
def mneme(message):
    bot.send_message(message.chat.id, "не буду🤣🤣🤣")


@bot.message_handler(func=lambda message: message.text.lower() == "сори")
def jdnd(message):
    bot.send_message(message.chat.id, "прощон")


@bot.message_handler(func=lambda message: message.text.lower() == "але")
def ale(message):
    bot.send_message(message.chat.id, "туда")


if __name__ == "__main__":
    print("🚀 Бот запущен (polling)")
    
    bot.infinity_polling(skip_pending=True)
