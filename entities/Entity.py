from datetime import date, datetime
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from dataclasses import dataclass

Base = declarative_base()

@dataclass
class Entity():
    '''Base Class for all entities while interacting with SQL'''
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)