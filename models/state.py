#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel,Base
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy import CHAR, DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models import storage_type
from models import storage
#from models.city import City

class State(BaseModel, Base):
    """ State class """
    if storage_type == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        # Relationship for DBStorage
        cities = relationship('City', backref='state', cascade='all, delete-orphan')
    else:
        name = ""

        def __init__(self, *args, **kwargs):
            """constructor  state"""
            super().__init__(*args, **kwargs)
        
        @property
        def cities(self):
            from models.city import City
            """Getter attribute cities that returns the list of City instances with state_id equals to the current State.id."""
            city_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
