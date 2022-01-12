from sqlalchemy import Column, String
from entities.Entity import Entity, Base

class ImageEntity(Entity, Base):
    __tablename__ = 'images'

    filename = Column(String)
    description = Column(String)

    def __init__(self, filename, description, created_by):
        Entity.__init__(self, created_by)
        self.filename = filename
        self.description = description