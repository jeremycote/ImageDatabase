import sqlite3
import os.path

connection = sqlite3.connect('database/database.db')

with open('database/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO images (filename, description) VALUES (?, ?)", ('images/Cake.jpg', "Delicious Cake!"))
cur.execute("INSERT INTO images (filename, description) VALUES (?, ?)", ('images/R1.jpg', "Robert Downey Jr."))

connection.commit()
connection.close()

