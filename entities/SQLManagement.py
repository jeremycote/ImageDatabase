from os import path
import sqlite3
from sqlite3.dbapi2 import connect
from PIL.Image import init
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from entities.Entity import Base
from entities.ImageEntity import ImageEntity, ImageSchema

from typing import List

from sqlalchemy import inspect

from database.init_db import init_db

class SQLManagement:
    def __init__(self, reload: bool = False) -> None:

        if reload:
            init_db()

        self.engine = create_engine('sqlite:///database/database.db')
        self.Session = sessionmaker(bind=self.engine)

        Base.metadata.create_all(self.engine)

    def reloadDatabase() -> None:
        '''Recreates Database using images folder'''
        init_db()

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

    def getImageEntitiesWithFilename(self, filename: str) -> List[ImageEntity]:
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