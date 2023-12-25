from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from src.delivery.containers import DeliveryContainer
from src.delivery.services.delivery import DeliveryService
from src.gateway.dependencies.jwt_auth import CustomJWTAuth

from utils.auth_operations import get_user_from_bearer

delivery_router = APIRouter()

user_auth = CustomJWTAuth()


@delivery_router.get('/get_orders', status_code=status.HTTP_200_OK)
@inject
async def get_orders(delivery_service: DeliveryService = Depends(Provide[DeliveryContainer.delivery_service]),
                     bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await delivery_service.get_orders(user_id)


@delivery_router.get('/get_order', status_code=status.HTTP_200_OK)
@inject
async def get_order(product: int,
                    delivery_service: DeliveryService = Depends(Provide[DeliveryContainer.delivery_service])):
    return await delivery_service.get_order(product)
