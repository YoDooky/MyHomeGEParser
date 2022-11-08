# from database.models import createdb
#
#
# db = createdb.DbCreator()
# conn = db.conn
# cur = db.cursor
#
# cur.execute("SELECT CASE WHEN EXISTS (SELECT * FROM Kobuleti LIMIT 1) THEN 1 ELSE 0 END")
# table_empty = cur.fetchone()[0]
# if table_empty:
#     print('+')
# print(table_empty)

import re
string_object = '1,300'
string_object = ''.join(string_object.split(','))
print(int(re.findall(r'\d+', string_object.strip())[0]))