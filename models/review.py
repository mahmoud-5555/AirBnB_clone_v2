#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from models import storage_type

class Review(BaseModel, Base):
    """ Review classto store review information """

    if storage_type == "db":
        __tablename__ = 'reviews'
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        def __init__(self, *args, **kwargs):
            """constructor Review"""
            super().__init__(*args, **kwargs)

        place_id = ""
        user_id = ""
        text = ""
