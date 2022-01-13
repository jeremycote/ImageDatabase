from sqlalchemy import Column, String
from marshmallow import Schema, fields
from entities.Entity import Entity, Base

class ImageEntity(Entity, Base):
    __tablename__ = 'images'

    filename = Column(String)
    path = Column(String)
    description = Column(String)

    def __init__(self, filename, description, path):
        Entity.__init__(self)
        self.filename = filename
        self.description = description
        self.path = path

class ImageSchema(Schema):
    '''Marshmallow Schema for JSON handling'''
    id = fields.Number()
    filename = fields.Str()
    description = fields.Str()
    path = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()