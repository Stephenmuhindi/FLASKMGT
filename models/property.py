#!/usr/bin/python3

import models
from models.base import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Properties(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'properties'
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        property_name = Column(String(128), nullable=False)
        adress = Column(String(128), nullable=True)
        make = Column(String(128), nullable=True)
    else:
        user_id =""
        property_name = ""
        adress = ""
        make = ""
