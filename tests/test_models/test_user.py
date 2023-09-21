#!/usr/bin/python3
""" """
import os
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """ """

    # def __init__(self, *args, **kwargs):
    #     """ Test doc """
    #     super().__init__(*args, **kwargs)
    #     self.name = "User"
    #     self.value = User

    # def test_first_name(self):
    #     """ Test doc """
    #     new = self.value()
    #     self.assertEqual(type(new.first_name), str)

    # def test_last_name(self):
    #     """ Test doc """
    #     new = self.value()
    #     self.assertEqual(type(new.last_name), str)

    # def test_email(self):
    #     """ Test doc """
    #     new = self.value()
    #     self.assertEqual(type(new.email), str)

    # def test_password(self):
    #     """ Test doc """
    #     new = self.value()
    #     self.assertEqual(type(new.password), str)
    def __init__(self, *args, **kwargs):
        """ user test class init"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ testing user first anme attr"""
        new = self.value()
        self.assertEqual(type(new.first_name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_last_name(self):
        """ testing user last name attr"""
        new = self.value()
        self.assertEqual(type(new.last_name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_email(self):
        """ testing user email attr"""
        new = self.value()
        self.assertEqual(type(new.email), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_password(self):
        """ testing user password attr"""
        new = self.value()
        self.assertEqual(type(new.password), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
