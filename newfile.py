import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand

API_TOKEN = "7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def set_commands():
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="music", description="Послушать музыку"),
    ]
    await bot.set_my_commands(commands)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши /music, чтобы послушать музыку.")

@dp.message(Command("music"))
async def cmd_music(message: types.Message):
    await message.answer("Подождите пару секунд...")

    # Строим путь к файлу, находящемуся рядом с этим .py файлом
    file_path = os.path.join(os.path.dirname(__file__), "zweielephanten.mp3")

    if os.path.exists(file_path):
        with open(file_path, "rb") as audio_file:
            await bot.send_audio(
                chat_id=message.chat.id,
                audio=audio_file,
                title="Zwei Elefanten",
                performer="Наталия Владимировна"
            )
    else:
        await message.answer("Файл музыки не найден 😢")

async def main():
    await set_commands()
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
