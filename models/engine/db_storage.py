#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
import os
"""This module defines a class to manage DB storage for hbnb clone"""


class DBStorage:
    """This class manages DB storage of hbnb models"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the db storage"""
        user = os.getenv('HBNB_MYSQL_USER')
        pswd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb//{}:{}@{}/{}'.format(
            user, pswd, host, db), pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)
            
    def all(self, cls):
        """Returns a dictionary of models currently in storage"""
        from models.amenity import Amenity
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User
        
        dictionary = {}       
        all_classes = [Amenity, City, Place, Review, State, User]
        if cls is None:
            for clsx in all_classes:
                q = self.__session.query(clsx)
                for item in q:
                    key = "{}.{}".format(type(item).__name__, item.id)
                    dictionary[key] = item
        else:
            if type(cls) == str:
                cls = eval(cls)
            q = self.__session.query(cls)
            for item in q:
                key = "{}.{}".format(type(item).__name__, item.id)
                dictionary[key] = item
                
        return dictionary
    
    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)
        
    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()
        
    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj is not None:
            self.__session.delete(obj)
            
    def reload(self):
        """Loads storage dictionary from DB"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()