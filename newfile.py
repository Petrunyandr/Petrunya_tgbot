import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BotCommand
import aiohttp

API_TOKEN = "7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs"  # Замените на токен вашего бота

# Ссылка на raw-версию MP3-файла с GitHub
GITHUB_AUDIO_URL = "https://github.com/Petrunyandr/Petrunya_tgbot/blob/main/zweielephanten.mp3"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Устанавливаем команды бота
async def set_commands():
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="music", description="Послушать музыку"),
    ]
    await bot.set_my_commands(commands)

# Обработка /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши /music, чтобы послушать музыку.")

# Обработка /music
@dp.message(Command("music"))
async def cmd_music(message: types.Message):
    await message.answer("Подождите пару секунд...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(GITHUB_AUDIO_URL) as resp:
                if resp.status == 200:
                    audio_bytes = await resp.read()
                    await bot.send_audio(
                        chat_id=message.chat.id,
                        audio=audio_bytes,
                        title="Zwei Elephanten",
                        performer="Наталия Владимировна"
                    )
                else:
                    await message.answer("Не удалось загрузить музыку с GitHub 😢")
    except Exception as e:
        await message.answer(f"Ошибка при загрузке аудио: {e}")

# Основной запуск
async def main():
    await set_commands()
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
