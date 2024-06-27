#!/usr/bin/python3
"""the __init__ module"""
import os

# Check the value of HBNB_TYPE_STORAGE environment variable
storage_type = os.getenv('HBNB_TYPE_STORAGE')
storage = None
if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    # Default to FileStorage if HBNB_TYPE_STORAGE is not set or has an invalid value
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Reload the storage after instantiation
storage.reload()
