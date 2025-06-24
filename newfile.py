import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.filters import Command

API_TOKEN = "7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

cached_audio_id = None  # Глобальная переменная для file_id аудио

# Устанавливаем команды бота (чтобы в меню отображались)
async def set_commands():
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="music", description="Послушать музыку"),
    ]
    await bot.set_my_commands(commands)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет!")

@dp.message(lambda message: message.text and message.text.lower() == "ку")
async def handle_ku(message: types.Message):
    await message.answer("нет")

@dp.message(Command("music"))
async def cmd_music(message: types.Message):
    global cached_audio_id
    await message.answer("Подождите пару секунд...")

    if cached_audio_id:
        # Отправляем кэшированное аудио по file_id
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=cached_audio_id,
            title="Zwei elefanten",
            performer="Наталия Владимировна"
        )
    else:
        # Отправляем файл и сохраняем file_id
        path = "/storage/emulated/0/Download/zweielephanten"  # путь к файлу
        with open(path, "rb") as voice:
            sent_message = await bot.send_audio(
                chat_id=message.chat.id,
                audio=voice,
                title="Zwei elefanten",
                performer="Наталия Владимировна"
            )
            cached_audio_id = sent_message.audio.file_id

async def main():
    await set_commands()
    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
