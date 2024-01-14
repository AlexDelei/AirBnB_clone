#!/usr/bin/env python3
"""My base model module"""
import uuid
from datetime import datetime
import models
from datetime import date


class BaseModel:
    """Parent class with

    3 public instance attrib
    3 methods
    """

    def __init__(self, *args, **kwargs):
        """Initializing public int attr"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ('created_at', ' updated_at'):
                    setattr(
                        self,
                        key,
                        datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                        )
                elif key == "__class__":
                    continue
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """Saves the updated time"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """dictionary"""
        d = {}
        for k, v in self.__dict__.items():
            if k == "created_at" or k == "updated_at":
                d[k] = v.strftime('%Y-%m-%dT%H:%M:%S.%f')
            else:
                d[k] = v
        d["__class__"] = self.__class__.__name__
        return d

    def __str__(self):
        """string representation of class"""
        return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id,
                self.__dict__
                )
