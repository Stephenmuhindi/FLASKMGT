#!/usr/bin/python3

from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.eng.db import DBStorage
    storage = DBStorage()
else:
    from models.eng.filestore import FileStorage
    storage = FileStorage()
storage.reload()
