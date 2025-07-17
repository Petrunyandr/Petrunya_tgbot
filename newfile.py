import telebot as t
from telebot import types
bot = t.TeleBot('7975402209:AAGilNMkPgXsoevUdWb-ZCovt2vOtPS9vGs')
bot.set_my_commands([
types.BotCommand("start", 'начать работу😁'),
types.BotCommand("music", 'послушать ')
])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "пр")
#сори

@bot.message_handler(func=lambda
message: message.text.lower() == "ку")
def ku(message):
	bot.send_message(message.chat.id, "нет")

bot.polling(none_stop=True)
