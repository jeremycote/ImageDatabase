import os.path

import sqlite3

from PIL import Image, ExifTags

from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from entities.Entity import Base
from entities.ImageEntity import ImageEntity, ImageSchema

from typing import List

from tqdm import tqdm

def createDb(imageInputPath: str = "images/raw") -> None:
    """Create a SQLite 3 .db file"""

    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, 'database.db')

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS images;
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, created_at NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at NOT NULL DEFAULT CURRENT_TIMESTAMP, filename TEXT NOT NULL, make TEXT, model TEXT, date TEXT, width INTEGER, height INTEGER)
    ''')

    imagePathsAbs = os.path.abspath(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), imageInputPath))
    print(imagePathsAbs)

    for file in tqdm(os.listdir(imagePathsAbs)):
        # cursor.execute("INSERT INTO images (filename) VALUES (?)", (file,))
        image = Image.open(os.path.join(imagePathsAbs, file))

        rawExif = image._getexif()

        if rawExif != None: 
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in image._getexif().items()
                if k in ExifTags.TAGS
            }

        info = [file]

        piece1 = "INSERT INTO images (filename"
        piece2 = ") VALUES (?"
        piece3 = ")"

        if rawExif:
            for attribute in ImageEntity.getExifAttributes():
                if attribute[1] in rawExif:
                    piece1 += ", " + attribute[0]
                    piece2 += ", ?"
                    info.append(exif[attribute[1]])
        cursor.execute(piece1 + piece2 + piece3, info)

    connection.commit()
    connection.close()

class SQLManagement:
    def __init__(self, reload: bool = False) -> None:

        if reload:
            createDb()

        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, 'database.db')
        self.engine = create_engine('sqlite:///' + db)
        self.Session = sessionmaker(bind=self.engine)

        Base.metadata.create_all(self.engine)

    def getElementWithId(self, id: int):
        # select * from table where id=id
        session = self.Session()
        data = session.query(ImageEntity).get(id)
        session.close()
        return data

    def getImageEntityWithId(self, id: int) -> ImageEntity:
        data = self.getElementWithId(id)
        schema = ImageSchema(many=False)
        image = schema.dump(data)
        return image

    def getElementsWithFilename(self, filename: str):
        # select * from table where id=id
        session = self.Session()
        data = session.query(ImageEntity).filter(ImageEntity.filename == filename)

        session.close()

        return data

    def getImageEntitiesWithFilename(self, filename: str):
        # select * from table where id=id
        data = self.getElementsWithFilename(filename)
        schema = ImageSchema(many=True)
        images = schema.dump(data)

        return images

    def getAllImageNames(self) -> List:
        session = self.Session()

        images = self.getAllImageRecords()

        paths = []
        for image in images:
            paths.append(image["filename"])

        session.close()
        return paths

    def getAllImageRecords(self) -> List:
        session = self.Session()
        image_objects = session.query(ImageEntity).all()

        # Convert SQL query to JSON-serializable objects
        schema = ImageSchema(many=True)
        images = schema.dump(image_objects)

        session.close()

        return images

    def addImageRecord(self, image: ImageEntity) -> None:
        session = self.Session()
        session.add(image)
        session.commit()