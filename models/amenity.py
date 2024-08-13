#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import relationship, backref
from models import storage_type

class Amenity(BaseModel, Base):
    if storage_type == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""
    def __init__(self, *args, **kwargs):
            """constructor  Amenity"""
            super().__init__(*args, **kwargs)
