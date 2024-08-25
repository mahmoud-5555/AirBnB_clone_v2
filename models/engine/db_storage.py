#!/usr/bin/python3

""" this module to deal with the sql databases """
from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.sql import select, insert, update, delete
from sqlalchemy import CHAR, DateTime, func
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import NoSuchTableError, OperationalError, ProgrammingError
from models.amenity import Amenity
from models.state import State
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from models.base_model import Base
from models.base_model import BaseModel
import os

class DBStorage:
    __engine = None
    __session = None
     
    def __init__(self):
        """ """
        mysql_user = os.getenv('HBNB_MYSQL_USER')
        mysql_pwd = os.getenv('HBNB_MYSQL_PWD')
        mysql_host = os.getenv('HBNB_MYSQL_HOST', default='localhost')
        mysql_db = os.getenv('HBNB_MYSQL_DB')

        # Construct the database URL
        # should change it after tested
        db_url = f"mysql+mysqldb://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}"

        # Create the engine
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        # Create a sessionmaker
        Session = sessionmaker(bind=self.__engine)

        # Create a session
        self.__session = Session()

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        this method must return a dictionary
        key = <class-name>.<object-id>
        value = object
        """
        
        data = {}
        if self.__session.is_active: #check if the session is open
            try:
                if cls:  #check  if class was passed to method
                    
                    objects = self.__session.query(cls).all()
                    for obj in objects:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        data[key] = obj
                else:
                    # Retrieve all objects from all classes
                    objects = self.__session.query(State).all() + \
                        self.__session.query(City).all() + \
                        self.__session.query(User).all() + \
                        self.__session.query(Place).all() + \
                        self.__session.query(Amenity).all() + \
                        self.__session.query(Review).all()
                    for obj in objects:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        data[key] = obj

            except NoSuchTableError as no_table:  #incase we wanna test where the error
                pass
            except OperationalError as OP_Error:
                pass
            except ProgrammingError as API_Error:
                pass
        return data

    def new(self, obj):
        """ add the object to the current database session """
        if obj is not None:
            if self.__session.is_active:  #check if the session is open
                try:
                    self.__session.add(obj)
                except NoSuchTableError as no_table:  #incase we wanna test where the error
                    pass
                except OperationalError as OP_Error:
                    pass
                except ProgrammingError as API_Error:
                    pass
                    
    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()
    
    def delete(self, obj=None):
        """"delete from the current database session obj if not None"""
        if obj is not None:
            if self.__session.is_active:  #check if the session is open
                try:
                    self.__session.delete(obj)
                except NoSuchTableError as no_table:  #incase we wanna test where the error
                    pass
                except OperationalError as OP_Error:
                    pass
                except ProgrammingError as API_Error:
                    pass
    
    def reload(self):
        """
        Create all tables in the database and create a new session.
        """
        # Create all tables in the database
        Base.metadata.create_all(self.__engine)

        # Create a sessionmaker with scoped_session
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

        try:
            # Attempt to commit any pending transactions
            self.__session.commit()
        except OperationalError:
            # Handle operational errors if any
            pass
    
    def close(self):
        self.__session.remove()