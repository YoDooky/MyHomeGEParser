import sqlite3
from typing import Dict, List
from config.server_config import DB_PATH
from database.models import createdb
from database.models.utils import format_data


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def insert_db(table: str, column_val: Dict):
    table = format_data.mod_string(table)  # replace spaces with underscore
    columns = ', '.join(column_val.keys())
    values = [tuple(column_val.values())]
    placeholders = ", ".join("?" * len(column_val.keys()))
    cursor.executemany(
        f"INSERT OR IGNORE INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int):
    row_id = int(row_id)
    cursor.execute(f"DELETE FROM {table} WHERE id={row_id}")
    conn.commit()


def sort(table: str, columns: List[str], filtr: str, order: str = 'DESC') -> List[Dict]:
    table = format_data.mod_string(table)  # replace spaces with underscore
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table} ORDER BY {filtr} {order}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def get_cursor():
    return cursor


def _init_db_():
    """Initialise DB"""
    db_creator = createdb.DbCreator()
    db_creator.__init_db__()


def check_db_exist():
    cursor.execute("SELECT name FROM sqlite_master "
                   f"WHERE type='table' AND name='cities'")
    table_cities_exists = cursor.fetchall()
    cursor.execute("SELECT name FROM sqlite_master "
                   f"WHERE type='table' AND name='users'")
    table_users_exists = cursor.fetchall()
    if table_cities_exists and table_users_exists:
        return
    _init_db_()


check_db_exist()
