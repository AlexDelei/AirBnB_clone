#!/usr/bin/env python3
"""My base model module"""
import uuid
from datetime import datetime
from models import storage

class BaseModel:
    """Parent class with

    3 public instance attrib
    3 methods
    """

    def __init__(self, *args, **kwargs):
        """Initializing public int attr"""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in('created_at', ' updated_at'):
                        setattr(self, key, datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def save(self):
        """Saves the updated time"""
        
        storage.save()

    def to_dict(self):
        """Converts to dictionary"""

        obj_dict = {
                'my_number': self.my_number,
                'name': self.name,
                '__class__': self.__class__.__name__,
                'updated_at': self.updated_at.isoformat(),
                'id': self.id,
                'created_at': self.created_at.isoformat()
                }
        return obj_dict
    
    def __str__(self):
        """string representation of class"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
