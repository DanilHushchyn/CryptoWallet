from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from propan import RabbitBroker
from starlette import status
from starlette.responses import Response

from config.settings import RABBITMQ_URL
from src.gateway.dependencies.jwt_auth import CustomJWTAuth
from src.wallet.containers import WalletContainer
from src.wallet.schemas import Transaction
from src.wallet.services.wallet import WalletService
from utils.auth_operations import get_user_from_bearer

wallet_router = APIRouter()

user_auth = CustomJWTAuth()


@wallet_router.get('/user_wallets', tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def user_wallets(user: int, wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service]),
                       bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    return await wallet_service.user_wallets(user)


@wallet_router.get('/get_wallet/{wallet_id}', tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def get_wallet(wallet_id: int, wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.get_wallet(wallet_id)


@wallet_router.post("/create_eth_wallet", tags=['wallet'], status_code=status.HTTP_201_CREATED)
@inject
async def create_eth_wallet(wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.create_user_wallet(user_id)


@wallet_router.post("/import_eth_wallet", tags=['wallet'], status_code=status.HTTP_201_CREATED)
@inject
async def import_eth_wallet(private_key: str,
                            wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service]),
                            bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.import_user_wallet(user_id, private_key)


@wallet_router.get("/wallet_balance", tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def wallet_balance(wallet_address: str,
                         wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service]),
                         bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    return await wallet_service.get_balance(wallet_address)


@wallet_router.put("/update_wallet_balance", tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def update_wallet_balance(wallet_address: str,
                                wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.update_balance(wallet_address)


@wallet_router.put("/update_all_wallets_balance", tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def update_all_wallets_balance(wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service]),
                                     bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await wallet_service.update_all(user_id)


@wallet_router.post("/send_eth", tags=['wallet'], status_code=status.HTTP_201_CREATED)
@inject
async def send_eth(trans: Transaction,
                   wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.transaction(from_address=trans.from_address,
                                            to_address=trans.to_address, value=trans.value)


@wallet_router.get('/wallet_db_transactions', tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def db_transactions(address: str,
                          wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    transactions = await wallet_service.get_db_transaction(address)
    transactions = transactions[::-1]
    return transactions


@wallet_router.get('/db_transactions', tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def get_all_transaction(wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.get_all_transaction()


@wallet_router.get('/transactions_moralis', tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def get_transactions(address: str,
                           wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    return await wallet_service.get_transactions(address)


@wallet_router.post('/load_wallet_trans', tags=['wallet'], status_code=status.HTTP_200_OK)
@inject
async def load_wallet_trans(address: str,
                            wallet_service: WalletService = Depends(Provide[WalletContainer.wallet_service])):
    await wallet_service.load_wallet_trans(address)
    return Response(content='Transactions updated via moralis', status_code=status.HTTP_200_OK)
