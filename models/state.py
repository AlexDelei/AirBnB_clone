#!/usr/bin/env python3
"""child class of BaseModel"""

from models.base_model import BaseModel


class State(BaseModel):
    """Holds the state"""

    def __init__(self, *args, **kwargs):
        """initialize public instances"""

        super().__init__(*args, **kwargs)
        self.name = ""
