from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Entity():
    '''Base Class for all entities while interacting with SQL'''
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    update_at = Column(DateTime)

    def __init__(self, created_by):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.last_updated_by = created_by