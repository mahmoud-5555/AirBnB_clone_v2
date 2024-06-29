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
import os

class DBStorage:
    """Database storage engine"""

    def __init__(self):
        """Initialize the database connection and session"""
        mysql_user = os.getenv('HBNB_MYSQL_USER', 'root')
        mysql_pwd = os.getenv('HBNB_MYSQL_PWD', '')
        mysql_host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        mysql_db = os.getenv('HBNB_MYSQL_DB', '')

        if not all([mysql_user, mysql_pwd, mysql_host, mysql_db]):
            raise ValueError("Missing one or more required environment variables")

        db_url = f"mysql+mysqldb://{mysql_user}:{mysql_pwd}@{mysql_host}/{mysql_db}"

        self.__engine = create_engine(db_url, pool_pre_ping=True)
        self.__session = None

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query and return all objects of a given class or all classes"""
        data = {}
        if self.__session.is_active:
            try:
                if cls:
                    objects = self.__session.query(cls).all()
                    for obj in objects:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        data[key] = obj
                else:
                    objects = self.__session.query(State).all() + \
                        self.__session.query(City).all() + \
                        self.__session.query(User).all() + \
                        self.__session.query(Place).all() + \
                        self.__session.query(Amenity).all() + \
                        self.__session.query(Review).all()
                    for obj in objects:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        data[key] = obj
            except (NoSuchTableError, OperationalError, ProgrammingError) as e:
                print(f"Error querying database: {e}")
        return data

    def new(self, obj):
        """Add the object to the current database session"""
        if obj is not None and self.__session.is_active:
            try:
                self.__session.add(obj)
            except (NoSuchTableError, OperationalError, ProgrammingError) as e:
                print(f"Error adding object to session: {e}")

    def save(self):
        """Commit all changes of the current database session"""
        try:
            self.__session.commit()
        except OperationalError as e:
            print(f"Error committing session: {e}")

    def delete(self, obj=None):
        """Delete the object from the current database session if not None"""
        if obj is not None and self.__session.is_active:
            try:
                self.__session.delete(obj)
            except (NoSuchTableError, OperationalError, ProgrammingError) as e:
                print(f"Error deleting object from session: {e}")

    def reload(self):
        """Create all tables in the database and create a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

        try:
            self.__session.commit()
        except OperationalError as e:
            print(f"Error committing session: {e}")
