#!/usr/bin/env python3
"""unittest for Testing Save in Basemodel"""
import unittest
import os
import json
from models.base_model import BaseModel
from models import storage
from datetime import datetime


class TestBaseModelSave(unittest.TestCase):
    """Testing my basemodel"""

    def setUp(self):
        """Setting up the class"""
        self.base_model = BaseModel()
        self.base_model.name = "Test Model"
        self.base_model.number = 42

    def tearDown(self):
        """Destroying the setup"""
        del self.base_model

    def test_save_updates_updated_at(self):
        """testting the updated_at attr"""
        filename = "file.json"
        data = storage.all()
        key = "BaseModel" + "." + BaseModel().id
        self.assertTrue(key in data)

    def test_save_creates_file_if_not_exists(self):
        """creating file if not there"""
        filename = "file.json"

        if os.path.isfile(filename):
            os.remove(filename)

        self.base_model.save()
        self.assertTrue(os.path.exists(filename))

    def test_save_updates_created(self):
        """testing created_at attribute"""
        old_created_at = self.base_model.created_at
        self.base_model.save()
        new_created_at = self.base_model.created_at

        self.assertEqual(old_created_at, new_created_at)

if __name__ == '__main__':
    unittest.main()
