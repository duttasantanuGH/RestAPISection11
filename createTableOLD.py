import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

createTable = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(createTable)

createTable = "CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(createTable)

#cursor.execute("INSERT INTO items VALUES (1, 'table', 14.99)")

connection.commit()
connection.close()