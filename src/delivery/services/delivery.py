import random
from propan import RabbitBroker
from config.settings import RABBITMQ_URL
# from config_socketio.google_requests import fetch, run_delivery
from src.delivery.models import Order
from src.delivery.repository import DeliveryRepository


class DeliveryService:
    def __init__(self, delivery_repository: DeliveryRepository) -> None:
        self._repository: DeliveryRepository = delivery_repository
    async def create_order(self, data):
        new_order = await self._repository.add(data)
        order = await self._repository.get_order(new_order.id)
        async with RabbitBroker(RABBITMQ_URL) as broker:
            data = {
                'id': order.id,
                'date': order.date,
                'status': order.status,
                'refund': order.refund,
                'transaction': order.transaction,
                'product': order.product,
                'product_price': order.product_price,
                'product_image': order.product_image,
                'room': new_order.user_id
            }
            await broker.publish(message=data, queue='socketio/new_order')

    async def get_order(self, order_id):
        return await self._repository.get_order(order_id)

    async def get_orders(self, user_id):
        return await self._repository.get_orders(user_id)
