#!/usr/bin/python3
""" Test doc"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State


class test_state(test_basemodel):
    """ Test doc"""

    def __init__(self, *args, **kwargs):
        """ Test doc"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ Test doc"""
        new = self.value()
        self.assertEqual(type(new.name), str)
