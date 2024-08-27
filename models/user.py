#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from models.base_model import Base
from sqlalchemy.orm import relationship, backref
from models import storage_type

class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if storage_type == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        __tablename__ = 'users'
        places = relationship("Place", backref="user",\
                          cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="user",\
                           cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        def __init__(self, *args, **kwargs):
            """constructor  City"""

            super().__init__(*args, **kwargs)
