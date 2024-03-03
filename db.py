import sqlite3
with sqlite3.connect('database.db') as db:
    cursor = db.cursor()
    # cursor.execute('''INSERT INTO users (id, username) VALUES (1235213, 'tesikшнгп')''')
    # cursor.execute('''SELECT username FROM users WHERE id = 1235213''')
    cursor.execute('''SELECT * FROM users''')
    print(cursor.fetchall())