#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel,Base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy import CHAR, DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from models.state import State
from sqlalchemy.orm import relationship, backref
from  models import storage_type


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if storage_type == 'db':
        __tablename__ = 'cities'
        __table_args__ = {'extend_existing': True}
        state_id = Column(String(128),ForeignKey(State.id), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="city",\
                          cascade="all, delete, delete-orphan")
    else:
        state_id = ""
        name = ""

        def __init__(self, *args, **kwargs):
            """constructor City"""
            super().__init__(*args, **kwargs)
