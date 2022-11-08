import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
CHAT_ID = -731369581

MAX_MENU_ITEMS = 30  # maximum amount of items to be showed in menu
MAX_AD_AMOUNT = 100  # maximum ad amount that would be load

WEBHOOK_PATH = f"/main/{TOKEN}"
APP_URL = os.getenv('APP_URL')
WEBHOOK_URL = APP_URL + WEBHOOK_PATH
BOT_URL = os.getenv('BOT_URL')
