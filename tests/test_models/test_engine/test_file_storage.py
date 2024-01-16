#!/usr/bin/env python3
"""unittest for Filestorage class"""
import unittest
import os
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class FileStorage_Test(unittest.TestCase):
    """Tests For the file storage class"""

    def setUp(self):
        """Creating a setup tests"""
        pass

    def tearDown(self):
        """Destroy All the tests"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_00_private_attrs(self):
        """Test to validate attribute are private"""
        fs = FileStorage()
        with self.assertRaises(AttributeError):
            print(fs.objects)
        with self.assertRaises(AttributeError):
            print(fs.file_path)

    def test_00a_id_attrs(self):
        """Test to validate attrs are private"""
        b = BaseModel()
        self.assertTrue(hasattr(b, "id"))
        self.assertEqual(type(b.id), str)

    def test_01a_all_return_type(self):
        """Test to validate all() returns a dict obj"""
        fs = FileStorage()
        self.assertEqual(type(fs.all()), dict)

    def test_01a_all_return_type(self):
        """tests to validate all() returns an empty dict"""
        fs = FileStorage()
        fs.new(BaseModel())
        self.assertTrue(fs.all())

    def test_02_working_save(self):
        """Test to validate save works"""
        fs = FileStorage()

        fs.new(BaseModel())
        fs.save()
        self.assertTrue(os.path.isfile("file.json"))

    def test_03_working_reload(self):
        """Test to validate reload works"""
        b = BaseModel()
        key = "BaseModel" + "." + b.id
        b.save()
        b1 = BaseModel()
        key1 = "BaseModel" + "." + b.id
        b1.save()
        self.assertTrue(storage.all()[key] is not None)
        self.assertTrue(storage.all()[key1] is not None)
        with self.assertRaises(KeyError):
            storage.all()[12345]

    def test_03a_working_reload(self):
        """Checks reload functionality if filePath doesnt exist"""
        fs = FileStorage()
        b = BaseModel()
        key = "BaseModel" + "." + b.id
        fs.new(b)
        fs.save()
        fs.reload()
        self.assertTrue(fs.all()[key])

    def test_04_working_new(self):
        """Testing if new method works"""
        fs = FileStorage()
        fs.new(BaseModel())
        self.assertTrue(fs.all())

    def test_05_new_int(self):
        """Passing integer to new method"""
        fs = FileStorage()
        with self.assertRaises(AttributeError):
            fs.new(1)

    def test_06_new_float(self):
        """passing a float"""
        fs = FileStorage()
        with self.assertRaises(AttributeError):
            fs.new(2.5)

    def test_07_new_inf(self):
        """Passing inf to new"""
        fs = FileStorage()
        with self.assertRaises(AttributeError):
            fs.new(float("inf"))

    def test_08_new_unknown(self):
        """Passes uknown to new"""
        fs = FileStorage()
        with self.assertRaises(NameError):
            fs.new(a)

    def test_09_new_nan(self):
        """passes nan to new"""
        fs = FileStorage()
        with self.assertRaises(AttributeError):
            fs.new(float("nan"))

    def test_10_new_string(self):
        """Passes string to new"""
        fs = FileStorage()
        with self.assertRaises(AttributeError):
            fs.new("string")

if __name__ == '__main__':
    unittest.main()
