#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


Base = declarative_base()


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    # DB Storage
    cities = relationship("City", backref='state',
                          cascade='all, delete, delete-orphan')

    # FileStorage
    @property
    def cities(self):
        """
        Returns the list of City instances with state_id equals to the
        current State.id
        """
        from models import storage
        all = storage.all()
        city_list = []
        result = []
        # Get only cities from file storage
        for key in all:
            import shlex
            city = key.replace(".", " ")
            city = shlex.split(city)
            if city[0] == "City":
                city_list.append(all[key])
        # Check if city.id is same with state.id
        for state in city_list:
            if state.state_id == self.id:
                result.append(state)
        return result
