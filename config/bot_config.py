import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
token = os.getenv('TOKEN')
chat_id = -731369581

max_menu_items = 30  # maximum amount of items to be showed in menu
max_ad_amount = 100  # maximum ad amount that woudl be load
