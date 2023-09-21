#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity
import os

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column(
        "place_id",
        String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "amenity_id",
        String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False,
    ),
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', cascade='all, delete, delete-orphan',
                               backref='place')
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Returns the list of Review instances with place_id equals to the
            current Place.id"""
            from models import storage
            all_reviews = storage.all(Review)
            result = []
            # Check if review.id is same with place.id
            for review in all_reviews.values():
                if review.place_id == self.id:
                    result.append(review)
            return result

        @property
        def amenities(self):
            """Returns the list of Amenity instances based on the attribute
            amenity_ids"""
            from models import storage
            all_reviews = storage.all(Review)
            result = []
            # Check if review.id is same with place.id
            for review in all_reviews.values():
                if review.place_id == self.id:
                    result.append(review)
            return result

        @amenities.setter
        def amenitites(self, amenity):
            """Handles append method for adding an Amenity.id to the attribute
            amenity_ids"""
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)
