import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

VERSION = "1^2"
