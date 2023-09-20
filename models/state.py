#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade='all, delete, delete-orphan',
                              backref='state')
    else:
        @property
        def cities(self):
            """
            Returns the list of City instances with state_id equals to the
            current State.id
            """
            from models import storage
            all_cities = storage.all(City)
            result = []
            # Check if city.id is same with state.id
            for city in all_cities.values():
                if city.state_id == self.id:
                    result.append(city)
            return result
