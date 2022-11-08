import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT')
