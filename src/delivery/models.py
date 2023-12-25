import datetime
# from sqladmin import ModelView
from sqlalchemy import *
from sqlalchemy.orm import relationship
from src.gateway.db import Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='NEW')

    refund_id = Column(Integer, ForeignKey('transactions.id'), nullable=True)
    refund = relationship('Transaction', foreign_keys=[refund_id])

    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    transaction = relationship('Transaction', foreign_keys=[transaction_id])

    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product', foreign_keys=[product_id])

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', foreign_keys=[user_id])
