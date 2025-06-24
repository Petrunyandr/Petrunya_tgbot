import telebot as t
from telebot import types

bot = t.TeleBot('7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs')

bot.set_my_commands([
types.BotCommand("/start",
"начать работy"),

types.BotCommand("/music", "послушать музыку ")
])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "пр")
#сори

@bot.message_handler(func=lambda
message: message.text.lower() == "ку")
def ku(message):
	bot.send_message(message.chat.id, "нет")


@bot.message_handler(commands=['music'])
def music(message):
	bot.send_message(message.from_user.id, "подождите пару секунд")
	voice = open('/storage/emulated/0/Download/zweielephanten', 'rb')
	bot.send_audio(message.chat.id,
	voice,
	title="Zwei elefanten",
	performer="Наталия Владимировна")
	voice.close()

bot.polling(none_stop=True)