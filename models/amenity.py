#!/usr/bin/env python3
"""child class of BaseModel"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """holds name amenity"""
    name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
