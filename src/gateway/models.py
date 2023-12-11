import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, MetaData
from sqlalchemy_utils import URLType

from config.settings import URL
from src.gateway.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    avatar = Column(URLType, nullable=True)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    chat_access = Column(Boolean, default=False)
