import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.utils import executor

TOKEN = '7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Установка команд бота
async def set_commands():
    commands = [
        BotCommand(command="/start", description="начать работу"),
        BotCommand(command="/music", description="послушать музыку"),
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("пр")
    # или await bot.send_message(message.from_user.id, "пр")

@dp.message_handler(lambda message: message.text and message.text.lower() == "ку")
async def ku(message: types.Message):
    await message.answer("нет")

@dp.message_handler(commands=['music'])
async def music(message: types.Message):
    await message.answer("подождите пару секунд")

    # Открываем файл асинхронно (лучше синхронно, но без блокировки main event loop)
    # Для простоты откроем синхронно, т.к. aiogram send_audio не поддерживает async stream
    with open('/storage/emulated/0/Download/zweielephanten', 'rb') as voice:
        await bot.send_audio(chat_id=message.chat.id,
                             audio=voice,
                             title="Zwei elefanten",
                             performer="Наталия Владимировна")

async def main():
    await set_commands()
    # Запуск бота
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
