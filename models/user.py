#!/usr/bin/env python3
"""Chlid class of BaseModel"""
from models.base_model import BaseModel


class User(BaseModel):
    """User Class inheriting from BaseModel"""

    def __init__(self, *args, **kwargs):
        """initializing user instances"""
        super().__init__(*args, **kwargs)
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""

    def to_dict(self):
        """Return Dictionary representation"""
        user_dict = super().to_dict()
        if self.email:
            user_dict['email'] = self.email
        if self.password:
            user_dict['password'] = self.password
        if self.first_name:
            user_dict['first_name'] = self.first_name
        if self.last_name:
            user_dict['last_name'] = self.last_name
        return user_dict

    def from_dict(self, data):
        """Update User attributes from dict"""
        super().from_dict(data)
        self.email = data.get('email', "")
        self.password = data.get('password', "")
        self.first_name = data.get('first_name', "")
        self.last_name = data.get('last_name', "")
