from dependency_injector.wiring import inject, Provide
from propan import RabbitRouter
from src.delivery.services.delivery import DeliveryService
from src.delivery.containers import DeliveryContainer

delivery_broker_router = RabbitRouter('delivery/')


@inject
async def delivery_service(service: DeliveryService = Provide[DeliveryContainer.delivery_service]):
    return service


@delivery_broker_router.handle('create_order')
async def delivery_handle(data):
    service: DeliveryService = await delivery_service()
    await service.create_order(data)
