import json
import os.path
from re import A

import sqlite3

from PIL import Image, ExifTags

from sqlalchemy import create_engine, MetaData, Table, or_
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

from entities.Entity import Base
from entities.ImageEntity import ImageEntity, ImageSchema


from typing import List

from tqdm import tqdm

from flask import jsonify

exifAttributes = [
    ("make", "Make", "TEXT"), ("model", "Model", "TEXT"), ("date", "DateTimeOriginal", "TEXT"), ("width", "ExifImageWidth", "INTEGER"), ("height", "ExifImageHeight", "INTEGER"),
    ("processingSoftware", "ProcessingSoftware", "TEXT"), ("documentName", "DocumentName", "TEXT"), ("imageDescription", "ImageDescription", "TEXT"), ("orientation", "Orientation", "INTEGER"), ("artist", "Artist", "TEXT"),
    ("copyright", "Copyright", "TEXT"), ("isoSpeed", "ISOSpeed", "INTEGER"), ("cameraOwnerName", "CameraOwnerName", "TEXT"), ("xPTitle", "XPTitle", "TEXT"), ("xPAuthor", "XPAuthor", "TEXT"),
    ("xPKeywords", "XPKeywords", "TEXT"), ("lensModel", "LensModel", "TEXT"), ("lensMake", "LensMake", "TEXT"), ("imageUniqueId", "ImageUniqueId", "TEXT")
]

class SQLManagement:
    def __init__(self, reload: bool = False) -> None:

        if reload:
            createDb()

        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, 'database.db')
        self.engine = create_engine('sqlite:///' + db)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(self.engine)

        self.images = Table("images",self.metadata,autoload = True, autoload_with=self.engine)

        print(self.images.columns.keys())

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
    
    def getImageEntitiesWithExif(self, exif: str):
        session = self.Session()

        # data = session.query(self.images).filter(or_(
        #     ImageEntity.filename.contains(exif),
        #     ImageEntity.make.contains(exif),
        #     ImageEntity.model.contains(exif),
        #     ImageEntity.date.contains(exif),
        #     ImageEntity.width.contains(exif),
        #     ImageEntity.height.contains(exif)
        # ))

        queries = []

        for attribute in exifAttributes:
            queries.append(self.images.c[attribute[0]].contains(exif))

        data = session.query(self.images).filter(or_(False, *queries)).all()

        results_as_dict = data.mappings().all()

        # search_args = [exif == self.images.c[col[0]] for col in exifAttributes]
        # data = session.query(self.images).filter(or_(*search_args)).all()
        # results_as_dict = data.mappings().all()
        # print(results_as_dict)
        # data = session.query(self.images).filter( exif in self.images.c[column[0]] for column in ImageEntity.getExifAttributes())
        # print(data)
        # schema = ImageSchema(many=True)
        # images = jsonify(data)
        
        session.close()

        return results_as_dict

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

def createDb(imageInputPath: str = "images/raw") -> None:
    """Create a SQLite 3 .db file"""

    path = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(path, 'database.db')

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute('''
        DROP TABLE IF EXISTS images;
    ''')

    sqlCommand = "CREATE TABLE IF NOT EXISTS images (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, created_at NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at NOT NULL DEFAULT CURRENT_TIMESTAMP, filename TEXT NOT NULL"
    
    # make TEXT, model TEXT, date DATETIME, width INTEGER, height INTEGER
    
    for snippet in exifAttributes:
        sqlCommand += ", " + snippet[0] + " " + snippet[2]

    print(sqlCommand)
    sqlCommand += ")"
    cursor.execute(sqlCommand)

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

        if exif:
            for attribute in exifAttributes:
                if attribute[1] in exif:

                    if attribute[1] == "DateTimeOriginal":
                        # Need to convert to sql and python compatible format
                        exif[attribute[1]] = formatDateTime(exif[attribute[1]])

                    piece1 += ", " + attribute[0]
                    piece2 += ", ?"
                    # print(attribute[1],": ", exif[attribute[1]])
                    info.append(exif[attribute[1]])
        cursor.execute(piece1 + piece2 + piece3, info)

    connection.commit()
    connection.close()

def formatDateTime(raw: str) -> str:
    datePieces = raw.split(" ")
    if len(datePieces) == 2:
        return datePieces[0].replace(":","-") + " " + datePieces[1].replace("-",":")
    else:
        return ""