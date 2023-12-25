from _decimal import Decimal
from typing import Callable
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.delivery.models import Order
from src.delivery.schemas import OrderForm


class DeliveryRepository:
    def __init__(self, session_factory: Callable[..., AsyncSession]) -> None:
        self.session_factory = session_factory

    async def add(self, data):
        async with self.session_factory() as session:
            order: Order = Order(
                product_id=data.get('product_id'),
                transaction_id=data.get('transaction_id'),
                user_id=data.get('user_id')
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order

    async def get_order(self, order_id):
        async with self.session_factory() as session:
            result = await session.execute(
                select(Order).options(joinedload(Order.product)).options(joinedload(Order.transaction)).options(
                    joinedload(Order.refund)).where(Order.id == order_id))
            order = result.scalar_one_or_none()
            if not order:
                raise HTTPException(status_code=401,
                                    detail=f"Product not found, id: {order_id}")
            return OrderForm(
                id=order.id,
                date=str(order.date),
                status=order.status,
                refund=order.refund.hash if order.refund else None,
                transaction=order.transaction.hash,
                product=order.product.title,
                product_price=Decimal(order.product.price),
                product_image=order.product.image
            )

    async def get_orders(self, user_id):
        async with self.session_factory() as session:
            result = await session.execute(
                select(Order).options(joinedload(Order.product)).options(joinedload(Order.transaction)).options(
                    joinedload(Order.refund)).where(Order.user_id == user_id))
            orders = result.scalars().all()
            return [OrderForm(
                id=order.id,
                date=str(order.date),
                status=order.status,
                refund=order.refund.hash if order.refund else None,
                transaction=order.transaction.hash,
                product=order.product.title,
                product_price=Decimal(order.product.price),
                product_image=order.product.image
            ) for order in orders]
