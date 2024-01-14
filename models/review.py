#!/usr/bin/env python3
"""child class of BaseModel"""
from models.base_model import BaseModel


class Review(BaseModel):
    """review info"""
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
