#!/usr/bin/python3
""" Test console module"""
import unittest
import console


class Test_Console(unittest.TestCase):
    """doc doc"""

    def test_documentation(self):
        """Test console documentation"""
        self.assertIsNotNone(console.__doc__)
