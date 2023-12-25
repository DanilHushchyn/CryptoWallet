from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from src.gateway.db import Base


class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    image = Column(URLType, nullable=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', foreign_keys=[user_id])
