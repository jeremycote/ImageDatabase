import os.path

import sqlite3

from PIL import Image, ExifTags

from sqlalchemy import create_engine, MetaData, Table, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from typing import List, Dict

from tqdm import tqdm

from src.constants import PATH_IMAGES_RAW, PATH_DB

exifAttributes = [
    ("make", "Make", "TEXT"), ("model", "Model", "TEXT"), ("date", "DateTimeOriginal", "TEXT"), ("width", "ExifImageWidth", "INTEGER"), ("height", "ExifImageHeight", "INTEGER"),
    ("processingSoftware", "ProcessingSoftware", "TEXT"), ("documentName", "DocumentName", "TEXT"), ("imageDescription", "ImageDescription", "TEXT"), ("orientation", "Orientation", "INTEGER"), ("artist", "Artist", "TEXT"),
    ("copyright", "Copyright", "TEXT"), ("isoSpeed", "ISOSpeed", "INTEGER"), ("cameraOwnerName", "CameraOwnerName", "TEXT"), ("xPTitle", "XPTitle", "TEXT"), ("xPAuthor", "XPAuthor", "TEXT"),
    ("xPKeywords", "XPKeywords", "TEXT"), ("lensModel", "LensModel", "TEXT"), ("lensMake", "LensMake", "TEXT"), ("imageUniqueId", "ImageUniqueId", "TEXT")
]

searchColumns = ["filename"] + [attribute[0] for attribute in exifAttributes]

Base = declarative_base()

class SQLManagement:
    """
    Handles all querries to SQL database using SQLAlchemy.
    """

    def __init__(self, reload: bool = False) -> None:
        """
        Initialize SQLManagement class.

        Args:
            reload (bool): Recreates database using files at PATH_IMAGES_RAW
        """
        if reload:
            createDb()

        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, 'database.db')
        self.engine = create_engine('sqlite:///' + db)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(self.engine)

        self.images = Table("images",self.metadata,autoload = True, autoload_with=self.engine)

        Base.metadata.create_all(self.engine)

    def getRowsWithValue(self, value: str, columns: List[str], maxRows: int = None, strict: bool = False) -> List[Dict[str,str]]:
        """Returns all rows in database where columns contain value.

        Args:
            value (str): value to search in database
            columns (List[str]): columns to search in
            strict (bool): exact matches only

        Returns:
            List[Dictionary[str,str]] - List of rows converted to dictionaries

        """

        session = self.Session()

        queries = []
        for column in columns:
            if strict:
                queries.append(self.images.c[column] == value)
            else:
                queries.append(self.images.c[column].contains(value))

        data = session.query(self.images).filter(or_(False, *queries))

        if (maxRows):
            data = data.limit(maxRows)

        data = data.all()

        session.close()

        return [dict(d) for d in data]

    def getAllValuesInColumn(self, column: str) -> List[str]:
        """Returns all values in a column.

        Args:
            column (str): column to return from database

        Returns:
            List[str]

        """

        session = self.Session()

        values = []
        for image in session.query(self.images).all():
            values.append(image[column])

        session.close()
        return values

    def getAllRows(self) -> List:
        """Returns all rows in database.

        Returns:
            List[Dictionary[str,str]] - List of rows converted to dictionaries

        """
        session = self.Session()

        rows = session.query(self.images).all()

        session.close()

        return [dict(row) for row in rows]

def createDb(imageInputPath: str = PATH_IMAGES_RAW) -> None:
    """
    Creates a SQLite 3 .db file. Drops existing tables.

    Args:
        imageInputPath (str): absolute path to input directory
    """

    connection = sqlite3.connect(PATH_DB)
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

    for file in tqdm(os.listdir(imageInputPath)):
        # cursor.execute("INSERT INTO images (filename) VALUES (?)", (file,))
        image = Image.open(os.path.join(imageInputPath, file))

        rawExif = image._getexif()

        info = [file]

        piece1 = "INSERT INTO images (filename"
        piece2 = ") VALUES (?"
        piece3 = ")"

        if rawExif != None: 
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in image._getexif().items()
                if k in ExifTags.TAGS
            }

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
    """
    Helper function. Converts Image exif datetime into Python datetime

    Args:
        raw (str): exif datetime string

    Returns:
        str - python compatible datetime string
    """
    
    datePieces = raw.split(" ")
    if len(datePieces) == 2:
        return datePieces[0].replace(":","-") + " " + datePieces[1].replace("-",":")
    else:
        return ""