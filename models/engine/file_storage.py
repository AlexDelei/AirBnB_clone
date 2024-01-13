#!/usr/bin/env python3
"""JSON serialization and deserialization"""
import json
import os
import logging
from importlib import import_module


class FileStorage:
    """File handling class"""

    __file_path = os.path.join("/AirBnB_clone/", "file.json")
    __objects = {}

    def all(self):
        """returns dictionary objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets the object with a certain key"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes the objects into JSON file"""
        serialized = {}
        for key, obj in FileStorage.__objects.items():
            serialized[key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(serialized, default=str) + '\n')

    def reload(self):
        """deserializes json file to objects"""
        try:
            with open(FileStorage.__file_path, 'r', encoding="utf-8") as fi:
                try:
                    data = json.load(fi)
                except json.JSONDecodeError as e:
                    logging.error("Invalid JSON data in file: %s", e)
                    return

                for key, value in data.items():
                    if '.' in key:
                        class_name, obj_id = key.split('.')
                    else:
                        class_name, obj_id = "User", key

                    module = import_module('models.user')
                    clas = getattr(module, class_name)
                    obj_instance = clas(**value)
                    FileStorage.__objects[key] = obj_instance

        except FileNotFoundError:
            pass
