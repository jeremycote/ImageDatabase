import sqlite3

connection = sqlite3.connect('/home/jeremy/Projects/ImageDatabase/database/database.db')

with open('/home/jeremy/Projects/ImageDatabase/database/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO images (filename, description) VALUES (?, ?)", ('Cake.jpg', "Delicious Cake!"))
cur.execute("INSERT INTO images (filename, description) VALUES (?, ?)", ('R1.jpg', "Robert Downey Jr."))

connection.commit()
connection.close()

