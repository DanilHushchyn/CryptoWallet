from sqlalchemy import Column, Integer
from src.gateway.db import Base


class Block(Base):
    __tablename__ = 'blocks'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=True)

