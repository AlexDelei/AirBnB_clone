#!/usr/bin/python

from models.base_model import BaseModel


class User(BaseModel):
    """user info"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
