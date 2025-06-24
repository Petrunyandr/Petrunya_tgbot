import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.filters import Command

API_TOKEN = "7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

cached_audio_id = None  # Здесь будет храниться file_id аудио

async def set_commands():
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="music", description="Послушать музыку"),
    ]
    await bot.set_my_commands(commands)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Напиши /music, чтобы послушать музыку.")

@dp.message(lambda message: message.text and message.text.lower() == "ку")
async def handle_ku(message: types.Message):
    await message.answer("нет")

@dp.message(Command("music"))
async def cmd_music(message: types.Message):
    await message.answer("Подождите пару секунд...")
    with open("/storage/emulated/0/zweielephanten", "rb") as audio_file:
    sent = await bot.send_audio(chat_id=message.chat.id,
    audio=audio_file,
    title="Zwei Elefanten",
    performer="Наталия Владимировна")
                cached_audio_id = sent.audio.file_id
        except FileNotFoundError:
            await message.answer("Файл zweielephanten.mp3 не найден!")

async def main():
    await set_commands()
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
