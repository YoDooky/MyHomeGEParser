import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
CHAT_ID = -731369581

MAX_MENU_ITEMS = 30  # maximum amount of items to be showed in menu
MAX_AD_AMOUNT = 100  # maximum ad amount that woudl be load

WEBHOOK_PATH = f"/main/{TOKEN}"
WEBHOOK_URL = "https://38eb-178-134-173-91.eu.ngrok.io" + WEBHOOK_PATH
BOT_PORT = os.getenv('BOT_PORT')
