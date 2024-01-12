#!/usr/bin/env python3
"""Testing if file is created"""

from models.engine.file_storage import FileStorage
from models.base_model import BaseModel

# instances of file_storage
storage = FileStorage()
storage.reload()

# an instance of the BaseModel
my_model = BaseModel(name="Example", my_number=42)

# adding model to storage
storage.new(my_model)
storage.save()
