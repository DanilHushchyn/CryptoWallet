from sqlalchemy import Column, String, DECIMAL, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from src.gateway.db import Base
class Blockchain(Base):
    __tablename__ = 'blockchains'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)
    image = Column(URLType, nullable=True)


class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String)
    image = Column(URLType, nullable=True)
    symbol = Column(String)
    decimal_places = Column(Integer, default=0)

    blockchain_id = Column(Integer, ForeignKey('blockchains.id'))
    blockchain = relationship('Blockchain', foreign_keys=[blockchain_id])


class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True, index=True)
    private_key = Column(String, unique=True)
    address = Column(String, unique=True)
    balance = Column(DECIMAL, default=0.000000000000000000)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', foreign_keys=[user_id])

    asset_id = Column(Integer, ForeignKey('assets.id'))
    asset = relationship('Asset', foreign_keys=[asset_id])




class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String)
    from_address = Column(String)
    to_address = Column(String)
    value = Column(DECIMAL)
    date = Column(String, default='PENDING')
    txn_fee = Column(DECIMAL, default=0.0)
    status = Column(String, default='PENDING')
