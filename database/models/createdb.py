import sqlite3
from config.server_config import db_path
from database.models.utils import format_data


class DbCreator:
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __create_user_catalog(self):
        with self.conn:
            self.cursor.execute("""CREATE TABLE users (
                            id integer PRIMARY KEY,
                            first_name text,
                            username text,
                            type text
                            )""")

    def __create_city_catalog(self):
        with self.conn:
            self.cursor.execute("""CREATE TABLE cities (
                            city text,
                            id integer PRIMARY KEY
                            )""")

    def create_city_db(self, city: str):
        city = format_data.mod_string(city)  # replace spaces with underscore
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {city} (
                            id integer PRIMARY KEY,
                            url text,
                            title text,
                            address text,
                            floor integer,
                            room integer,
                            bedroom integer,
                            size integer,
                            price integer,
                            date text,
                            img_url text
                            )""")

    def __init_db__(self):
        try:
            self.__create_user_catalog()
        except sqlite3.OperationalError:
            self.__create_city_catalog()
