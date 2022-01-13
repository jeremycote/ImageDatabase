import sqlite3
import os.path
from PIL.Image import init

from tqdm import tqdm

def init_db():
    connection = sqlite3.connect('database/database.db')

    with open('database/schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()

    for file in tqdm(os.listdir("images/raw")):
        cur.execute(f"INSERT INTO images (filename, description, path) VALUES (?, ?, ?)", (file, "Description", "images/" + file))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()

