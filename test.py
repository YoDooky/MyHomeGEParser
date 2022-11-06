# import time
# from console_progressbar import ProgressBar
#
# pb = ProgressBar(total=10, prefix='Here', suffix='Now', decimals=0, length=50, fill='X', zfill='-')
# for i in range(10):
#     pb.print_progress_bar(i)
#     time.sleep(1)
# import sqlite3
# from config.server_config import db_path

# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()
# #
# # cursor.execute("""CREATE TABLE test (
# #                             id integer PRIMARY KEY,
# #                             date text
# #                             )""")
# # conn.commit()
# cursor.execute(
#     f"INSERT INTO test "
#     f"(id, date) "
#     f"VALUES (?,?)",
#     (5, '13.05 16:27'))
# conn.commit()
# from typing import List

all_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
cntr = 0


def slice_cities_list(max_len: int, choice: str = 'next'):
    print(all_list[0:max_len])
    counter = 0
    while True:
        choice = input('"next" or "back" ?: ')
        if choice == 'next':
            counter = min(counter + max_len, len(all_list) - 1)
            new_list = all_list[counter:counter + max_len]
        else:
            counter = max(counter - max_len, 0)
            new_list = all_list[counter: counter + max_len]

        print(new_list)
        # counter = min(counter + max_len, counter - len(all_list))


slice_cities_list(2)
