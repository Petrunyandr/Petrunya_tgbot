import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand, FSInputFile

API_TOKEN = "7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs"  # 🔐 Замени на свой токен от @BotFather

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Устанавливаем команды бота
async def set_commands():
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="music", description="Слушать музыку"),
    ]
    await bot.set_my_commands(commands)

# Обработка команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши /music, чтобы послушать музыку 🎶")

# Обработка команды /music
@dp.message(Command("music"))
async def cmd_music(message: types.Message):
    await message.answer("🎧 Подождите пару секунд, загружаю музыку...")

    # Путь к файлу
    path = os.path.join(os.path.dirname(__file__), "zweielephanten.mp3")

    # Проверка существования
    if os.path.exists(path):
        audio = FSInputFile(path)
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=audio,
            title="Zwei Elefanten",
            performer="Наталия Владимировна"
        )
    else:
        await message.answer("😢 Музыка не найдена. Убедитесь, что файл рядом с bot.py")

# Запуск
async def main():
    await set_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
