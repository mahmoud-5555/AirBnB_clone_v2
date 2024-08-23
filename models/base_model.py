#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from models import storage_type
from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy import CHAR, DateTime,func
from sqlalchemy.orm import declarative_base



if storage_type == 'db':
    Base = declarative_base()
else:
    Base = object

class BaseModel:
    """A base class for all hbnb models"""
    if storage_type == 'db':
        __abstract__ = True
        id = Column(String(60), primary_key=True,nullable=False,default=lambda: str(uuid.uuid4()))
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        
        if not kwargs :
            # from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
        else:
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.utcnow()
            else:
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%f")

            if 'updated_at' not in kwargs:
                self.updated_at = self.created_at
            else:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'], "%Y-%m-%dT%H:%M:%S.%f")

            # Convert 'created_at' if it exists
            if '__class__' in kwargs:
                del kwargs['__class__']

            self.__dict__.update(kwargs)
     

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def __repr__(self):
        """ The represintation of the object as string while printed """
        repdict = self.__dict__.copy()
        repdict.pop('_sa_instance_state', None)
        return '[{}] ({}) {}'.format(self.__class__.__name__, self.id, repdict)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        if  '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        from models import storage
        storage.delete(self)
