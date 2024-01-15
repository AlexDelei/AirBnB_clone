#!/usr/bin/env python3
"""Cty unittest"""
import unittest
import os
import pep8
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):
    """Testing the cty class"""

    @classmethod
    def setUpClass(cls):

        cls.city = City()
        cls.city.name = "Naivasha"
        cls.city.state_id = "Nakuru"

    @classmethod
    def teardown(cls):

        del cls.city

    def tearDown(self):
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_City(self):
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/city.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_City(self):
        self.assertIsNone(City.__doc__)

    def test_attributes_City(self):
        self.assertTrue('id' in self.city.__dict__)
        self.assertTrue('created_at' in self.city.__dict__)
        self.assertTrue('updated_at' in self.city.__dict__)
        self.assertTrue('state_id' in self.city.__dict__)
        self.assertTrue('name' in self.city.__dict__)

    def test_is_subclass_City(self):
        self.assertTrue(issubclass(self.city.__class__, BaseModel), True)

    def test_attribute_types_City(self):
        self.assertEqual(type(self.city.name), str)
        self.assertEqual(type(self.city.state_id), str)

    def test_save_City(self):
        self.city.save()
        self.assertNotEqual(self.city.created_at, self.city.updated_at)

    def test_to_dict_City(self):
        self.assertEqual('to_dict' in dir(self.city), True)


if __name__ == "__main__":
    unittest.main()
