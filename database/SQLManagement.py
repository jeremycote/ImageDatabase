import os.path

import sqlite3

from PIL import Image, ExifTags

from sqlalchemy import create_engine, MetaData, Table, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from typing import List, Dict

from tqdm import tqdm

exifAttributes = [
    ("make", "Make", "TEXT"), ("model", "Model", "TEXT"), ("date", "DateTimeOriginal", "TEXT"), ("width", "ExifImageWidth", "INTEGER"), ("height", "ExifImageHeight", "INTEGER"),
    ("processingSoftware", "ProcessingSoftware", "TEXT"), ("documentName", "DocumentName", "TEXT"), ("imageDescription", "ImageDescription", "TEXT"), ("orientation", "Orientation", "INTEGER"), ("artist", "Artist", "TEXT"),
    ("copyright", "Copyright", "TEXT"), ("isoSpeed", "ISOSpeed", "INTEGER"), ("cameraOwnerName", "CameraOwnerName", "TEXT"), ("xPTitle", "XPTitle", "TEXT"), ("xPAuthor", "XPAuthor", "TEXT"),
    ("xPKeywords", "XPKeywords", "TEXT"), ("lensModel", "LensModel", "TEXT"), ("lensMake", "LensMake", "TEXT"), ("imageUniqueId", "ImageUniqueId", "TEXT")
]

searchColumns = ["filename"] + [attribute[0] for attribute in exifAttributes]

Base = declarative_base()

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

    def getRowsWithValue(self, value: str, columns: List[str], maxRows: int = None) -> List[Dict[str,str]]:
        """Returns rows as dicts where columns contain value.

        Args:
            value (str): value to search in database
            columns (List[str]): columns to search in

        Returns:
            list of rows as dictionaries

        """

        session = self.Session()

        queries = []
        for column in columns:
            queries.append(self.images.c[column].contains(value))

        data = session.query(self.images).filter(or_(False, *queries))

        if (maxRows):
            data = data.limit(maxRows)

        data = data.all()

        session.close()

        return [dict(d) for d in data]

    def getAllValuesInColumn(self, column: str) -> List[str]:
        session = self.Session()

        values = []
        for image in session.query(self.images).all():
            values.append(image[column])

        session.close()
        return values

    def getAllRows(self) -> List:
        session = self.Session()

        rows = session.query(self.images).all()

        session.close()

        return [dict(row) for row in rows]

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