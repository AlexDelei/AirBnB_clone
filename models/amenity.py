#!/usr/bin/env python3
"""child class of BaseModel"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """holds amenities"""

    def __init__(self, *args, **kwargs):
        """initializing its public instances"""

        super().__init__(*args, **kwargs)
        self.name = ""
