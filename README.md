# Petrunya\_tgbot

Простой Telegram-бот на Python, созданный с использованием библиотеки [telebot](https://github.com/eternnoir/pyTelegramBotAPI).

---

## Возможности бота

* Отвечает на команду `/start`
* Отправляет музыку по команде `/music`

---

## Команды

| Команда  | Описание         |
| -------- | ---------------- |
| `/start` | Приветствие      |
| `/music` | Послушать музыку |

---

## Установка и запуск

### Для Android (Pydroid / Termux)

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/Petrunyandr/Petrunya_tgbot.git
   cd Petrunya_tgbot
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` в корне проекта и добавьте туда токен вашего бота:

   ```
   BOT_TOKEN=ваш_токен_от_BotFather
   ```

4. Запустите бота:

   ```bash
   python bot.py
   ```

---

## Развёртывание на Render

1. Подключите GitHub-репозиторий к Render.

2. Создайте новый Web Service.

3. В настройках окружения добавьте переменную:

   ```
   BOT_TOKEN=ваш_токен
   ```

4. В поле Start Command укажите:

   ```
   python bot.py
   ```

---

## Зависимости

* telebot
* python-dotenv

---

## Безопасность

* Никогда не храните токен бота в открытом коде или репозитории.
* Используйте файл `.env` для хранения токена.
* Добавьте `.env` в `.gitignore`, чтобы не залить его на GitHub.

---

## Автор

[@Petrunyandr](https://github.com/Petrunyandr)


