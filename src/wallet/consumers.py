from celery.result import AsyncResult
from dependency_injector.wiring import inject, Provide
from propan import RabbitRouter
from src.wallet.containers import WalletContainer
from src.wallet.services.wallet import WalletService

wallet_broker_router = RabbitRouter('wallet/')


@inject
async def wallet_service(service: WalletService = Provide[WalletContainer.wallet_service]):
    return service


@wallet_broker_router.handle('buy_product')
async def buy_product(data):
    service: WalletService = await wallet_service()
    await service.buy_product(data)
