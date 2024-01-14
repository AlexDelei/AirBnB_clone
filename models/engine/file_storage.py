#!/usr/bin/env python3
"""JSON serialization and deserialization"""
import json
from os import path
import logging
from models.base_model import BaseModel
from importlib import import_module
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """File handling class"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns dictionary objects"""
        return self.__objects

    def new(self, obj):
        """sets the object with a certain key"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serializes the objects into JSON file"""
        serialized = {}
        for key, obj in self.__objects.items():
            serialized[key] = obj.to_dict()

        with open(self.__file_path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(serialized, default=str) + '\n')

    def reload(self):
        """deserializes json file to objects"""
        if path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as f:
                for key, value in json.load(f).items():
                    self.new(classes[value['__class__']](**value))
