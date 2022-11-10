# import sqlite3
# from config.server_config import DB_PATH
from database.models.utils import format_data
import psycopg2
from config import db_config


# class DbCreator:
#     def __init__(self):
#         self.conn = sqlite3.connect(DB_PATH)
#         self.cursor = self.conn.cursor()
#
#     def __create_user_catalog(self):
#         with self.conn:
#             self.cursor.execute("""CREATE TABLE users (
#                             id integer PRIMARY KEY,
#                             first_name text,
#                             username text,
#                             type text
#                             )""")
#
#     def __create_city_catalog(self):
#         with self.conn:
#             self.cursor.execute("""CREATE TABLE cities (
#                             city text,
#                             id integer PRIMARY KEY
#                             )""")
#
#     def create_city_db(self, city: str):
#         city = format_data.mod_string(city)  # replace spaces with underscore
#         with self.conn:
#             self.cursor.execute(f"""CREATE TABLE {city} (
#                             id integer PRIMARY KEY,
#                             url text,
#                             title text,
#                             address text,
#                             floor integer,
#                             room integer,
#                             bedroom integer,
#                             size integer,
#                             price integer,
#                             date text,
#                             img_url text
#                             )""")
#
#     def __init_db__(self):
#         try:
#             self.__create_user_catalog()
#         except sqlite3.OperationalError:
#             self.__create_city_catalog()


class DbCreator:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=db_config.HOST,
            dbname=db_config.DB_NAME,
            user=db_config.USER,
            password=db_config.PASSWORD,
            port=db_config.DB_PORT,

        )
        # self.conn.set_client_encoding('UTF8')
        self.cursor = self.conn.cursor()

    def __create_user_catalog(self):
        with self.conn:
            self.cursor.execute("""CREATE TABLE users (
                            id bigint PRIMARY KEY,
                            first_name text,
                            username text,
                            type text
                            )""")

    def __create_city_catalog(self):
        with self.conn:
            self.cursor.execute("""CREATE TABLE cities (
                            city text,
                            id bigint PRIMARY KEY
                            )""")

    def create_city_db(self, city: str):
        city = format_data.mod_string(city)  # replace spaces with underscore
        with self.conn:
            self.cursor.execute(f"""CREATE TABLE {city} (
                            id bigint PRIMARY KEY,
                            url text,
                            title text,
                            address text,
                            floor varchar(10),
                            room varchar(10),
                            bedroom varchar(10),
                            size int,
                            price int,
                            date text,
                            img_url text
                            )""")

    def __init_db__(self):
        try:
            self.__create_user_catalog()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create users database, trying to create city catalog...\n'
                  f'[ERR] {ex}')
        try:
            self.__create_city_catalog()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create cities database, trying to create city catalog...\n'
                  f'[ERR] {ex}')

