from ast import Str
from dataclasses import dataclass
from sqlalchemy import Column, String, DateTime, Integer
from marshmallow import Schema, fields
from entities.Entity import Entity, Base
from datetime import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass

# @dataclass
class ImageEntity(Entity, Base):
    __tablename__ = 'images'

    filename = Column(String)
    

    def __init__(self, filename: str, exif: Dict[str,str]):
        self.filename = filename
        self.exif = exif


class ImageSchema(Schema):
    '''Marshmallow Schema for JSON handling'''
    id = fields.Number()
    filename = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    exif = fields.Dict(keys=fields.Str(), values=fields.Str())
    # make = fields.Str()
    # model = fields.Str()
    # date = fields.DateTime()
    # width = fields.Number()
    # height = fields.Number()
    # processingSoftware = fields.Str()
    # documentName = fields.Str()
    # imageDescription = fields.Str()
    # orientation = fields.Str()
    # artist = fields.Str()
    # copyright = fields.Str()
    # isoSpeed = fields.Number()
    # cameraOwnerName = fields.Str()
    # xPTitle = fields.Str()
    # xPAuthor = fields.Str()
    # xPKeywords = fields.Str()
    # lensModel = fields.Str()
    # lensMake = fields.Str()
    # imageUniqueId = fields.Str()