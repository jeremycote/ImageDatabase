from sqlalchemy import Column, String
from marshmallow import Schema, fields
from entities.Entity import Entity, Base

class ImageEntity(Entity, Base):
    __tablename__ = 'images'

    filename = Column(String)
    description = Column(String)

    def __init__(self, filename, description):
        Entity.__init__(self)
        self.filename = filename
        self.description = description

class ImageSchema(Schema):
    '''Marshmallow Schema for JSON handling'''
    id = fields.Number()
    filename = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()