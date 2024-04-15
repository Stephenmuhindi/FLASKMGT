#!/usr/bin/python3

import models
from models.base import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5
from flask_login import UserMixin

class User(BaseModel, UserMixin, Base):
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        properties = relationship("Properties", backref="user", cascade="all, delete-orphan")
    else:
        email = ""
        password = ""
