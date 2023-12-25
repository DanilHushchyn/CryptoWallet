from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from src.gateway.dependencies.jwt_auth import CustomJWTAuth
from src.ibay.containers import IbayContainer
from src.ibay.schemas import BuyProduct, ProductForm
from src.ibay.services.ibay import IBayService
from utils.auth_operations import get_user_from_bearer

product_router = APIRouter()

user_auth = CustomJWTAuth()


@product_router.post('/add_product', status_code=status.HTTP_201_CREATED)
@inject
async def add_product(product: ProductForm, ibay_service: IBayService = Depends(Provide[IbayContainer.ibay_service]), bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await ibay_service.add_product(product, user_id)


@product_router.get('/get_products', status_code=status.HTTP_200_OK)
@inject
async def get_products(ibay_service: IBayService = Depends(Provide[IbayContainer.ibay_service])):
    return await ibay_service.get_products()


@product_router.get('/get_product', status_code=status.HTTP_200_OK)
@inject
async def get_product(product: int, ibay_service: IBayService = Depends(Provide[IbayContainer.ibay_service])):
    return await ibay_service.get_product(product)


@product_router.post('/buy_product', status_code=status.HTTP_200_OK)
@inject
async def buy_product(buy: BuyProduct, ibay_service: IBayService = Depends(Provide[IbayContainer.ibay_service]), bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await ibay_service.buy_product(buy, user_id)