#!/usr/bin/env python3
"""child class of BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Look at details"""

    def __init__(self, *args, **kwargs):
        """initialising public instances"""

        self.place_id = ""
        self.user_id = ""
        self.text = ""
