#!/usr/bin/env python3
"""My base model module"""
import uuid
from datetime import datetime


class BaseModel:
    """Parent class with

    3 public instance attrib
    3 methods
    """

    def __init__(self, my_number=None, name=None):
        """Initializing public int attr"""

        self.id = str(uuid.uuid4())
        self.my_number = my_number
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Saves the updated time"""
        
        self.updated_at = datetime.now()

    def to_dict(self):
        """Converts to dictionary"""

        obj_dict = self.__dict__
        obj_dict['id'] = self.id
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict
    
    def __str__(self):
        """string representation of class"""
        return "[{}] {}) {} {}".format(self.__class__.__name__, self.my_number, self.name, self.__dict__)
