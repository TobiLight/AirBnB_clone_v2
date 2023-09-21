#!/usr/bin/python3
"""Module for testing DB storage"""
from models.engine.db_storage import DBStorage
import os
import unittest


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "Test is not relevant for DBStorage"
)
class test_DB_Storage(unittest.TestCase):
    """testing"""

    def test_documentation(self):
        """test document"""
        self.assertIsNot(DBStorage.__doc__, None)
