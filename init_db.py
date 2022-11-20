import sqlite3

connection = sqlite3.connect('solar_powered_kangoo.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
