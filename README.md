# Petrunya_tgbot

Это простой Telegram-бот на Python,созданный с использованием библиотеки [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).  
Бот умеет:

- Отвечать на команду `/start`
- Отправлять музыку по команде `/music`

## 🚀 Команды бота

/start -прииаетсвие
/music - послушать музыку

## Установка и запуск

### Для Android (Pydroid / Termux)

1. Склонируй репозиторий:
   ```bash
   git clone https://github.com/Petrunyandr/Petrunya_tgbot.git
   cd Petrunya_tgbot

2. Установи зависимости:

pip install -r requirements.txt


3. Создай .env файл и добавь туда токен:

BOT_TOKEN=твой_токен_от_BotFather


4. Запусти бота:

python bot.py




Развёртывание на Render

1. Подключи GitHub-репозиторий к Render


2. Создай новый Web Service


3. В Environment добавь переменную:

BOT_TOKEN=твой_токен


4. Укажи Start Command:

python bot.py





Зависимости

pyTelegramBotAPI

python-dotenv

requests


Все они указаны в requirements.txt.



Безопасность

Никогда не загружай токен в код или в репозиторий

Используй .env для хранения токена

Убедись, что .env добавлен в .gitignore




Автор

@Petrunyandr




Лицензия

MIT License. Свободно для использования и модификации.


