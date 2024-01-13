#!/usr/bin/env python3
"""Child class of BasModel"""
from models.base_model import BaseModel


class City(BaseModel):
    """holds city name"""

    def __init__(self, *args, **kwargs):
        """initialising public instances"""

        super().__init__(*args, **kwargs)
        self.state_id = ""
        self.name = ""
