import asyncio
import telebot as t
from telebot import types

bot = t.AsyncTeleBot('7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs')

bot.set_my_commands([
types.BotCommand("/start",
"начать работy"),

types.BotCommand("/music", "послушать музыку ")
])


@bot.message_handler(commands=['start'])
async def start(message):
	await
	bot.send_message(message.from_user.id, "пр")
#сори

@bot.message_handler(func=lambda
message: message.text and message.text.lower() == "ку")
async def ku(message):
	await
	bot.send_message(message.chat.id, "нет")


@bot.message_handler(commands=['music'])
async def music(message):
	await 
	bot.send_message(message.from_user.id, "подождите пару секунд")
	voice = open('/storage/emulated/0/Download/zweielephanten', 'rb')
	await
	bot.send_audio(message.chat.id,
	voice,
	title="Zwei elefanten",
	performer="Наталия Владимировна")
	voice.close()
async def main():
	await bot.set_webhook()  # если используешь webhook, иначе можно убрать
	await bot.polling()

if __name__ == '__main__':
	asyncio.run(main())
	bot.polling(none_stop=True)
