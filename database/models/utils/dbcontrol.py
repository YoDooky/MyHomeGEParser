from typing import Dict, List
from database.models import createdb
from database.models.utils import format_data

database = createdb.DbCreator()
conn = database.conn
cursor = database.cursor


def insert_db(table: str, column_val: Dict):
    """Inser data to DB"""
    table = format_data.mod_string(table)  # replace spaces with underscore
    columns = ', '.join(column_val.keys())
    values = tuple(map(str, column_val.values()))
    cursor.execute(
        f"INSERT INTO {table.lower()} "
        f"({columns}) "
        f"VALUES {values} "
        f"ON CONFLICT (id) DO NOTHING"
    )
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    """Get selected columns from DB"""
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table.lower()}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int):
    """Delete data by ID from DB"""
    row_id = int(row_id)
    cursor.execute(f"DELETE FROM {table} WHERE id={row_id}")
    conn.commit()


def sort(table: str, columns: List[str], filtr: str, order: str = 'DESC') -> List[Dict]:
    """Sort data by column (ASC or DSC)"""
    table = format_data.mod_string(table)  # replace spaces with underscore
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table.lower()} ORDER BY {filtr} {order}")
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


def check_table_empty(table: str) -> int:
    """Check table is empty or not"""
    cursor.execute(f"SELECT CASE WHEN EXISTS (SELECT * FROM {table} LIMIT 1) THEN 1 ELSE 0 END")
    table_not_empty = cursor.fetchone()[0]
    return table_not_empty


def check_table_exist(table: str) -> bool:
    """Check if table exist"""
    cursor.execute("SELECT EXISTS (SELECT * FROM information_schema.tables "
                   f"WHERE table_schema = 'public' AND table_name  = '{table.lower()}');")
    if cursor.fetchone()[0]:
        return True


def check_db_exist():
    table_cities_exist = check_table_exist('cities')
    table_users_exist = check_table_exist('users')
    if table_cities_exist and table_users_exist:
        return
    _init_db_()


check_db_exist()
