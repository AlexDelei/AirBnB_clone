#!/usr/bin/env python3
"""JSON serialization and deserialization"""
import json


class FileStorage:
    """File handline case"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns dictionary objects"""

        return FilesStorage.__objects

    def new(self, obj):
        """sets the object with a certain key"""

        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes the objects into JSON file"""

        serialized = {}
        for key, value in FileStorage.__objects.items():
            serialized[key] = obj.to_dict

        with open(FileStorage.__file_path, 'w', encoding="utf-8") as f:
            json.dump(serialized, f, default=str)

    def reload(self):
        """deserializes json file to objects"""

        try:
            with open(FileStorage.__file_path, 'r', encoding="utf-3") as fi:
                data = json.load(fi)

                for key, value in data.items():
                    class_name, obj.id = key.split('.')
                    module = __import__('models.' + class_name, fromlist=[class_name])
                    cls = getattr(module, class_name)
                    obj_instance = cls_(**value)
                    FileStorage.__object[key] = obj_instance
        except FileNotFoundError:
            pass
