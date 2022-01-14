from dataclasses import dataclass
from sqlalchemy import Column, String, DateTime, Integer
from marshmallow import Schema, fields
from entities.Entity import Entity, Base
from datetime import datetime
from typing import List
from dataclasses import dataclass

@dataclass
class ImageEntity(Entity, Base):
    __tablename__ = 'images'

    filename = Column(String)
    make = Column(String)
    model = Column(String)
    date = Column(DateTime)
    width = Column(Integer)
    height = Column(Integer)

    @staticmethod
    def getExifAttributes() -> List[str]:
        return [("make", "Make"), ("model", "Model"), ("date", "DateTimeOriginal"), ("width", "ExifImageWidth"), ("height", "ExifImageHeight")]

class ImageSchema(Schema):
    '''Marshmallow Schema for JSON handling'''
    id = fields.Number()
    filename = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()