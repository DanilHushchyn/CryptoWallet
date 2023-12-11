from dependency_injector import containers, providers

from config.settings import WIRING_CONFIG
from src.gateway.containers import DatabaseContainer
from src.wallet.repository import WalletRepository
from src.wallet.services.wallet import WalletService
from src.web3.web3_service import WebService


class WalletContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    wallet_repository = providers.Factory(WalletRepository, session_factory=DatabaseContainer.session)
    # web3_repository = providers.Factory(WebRepository, session_factory=DatabaseContainer.session)
    w3_service = providers.Singleton(WebService)
    wallet_service = providers.Factory(WalletService, wallet_repository=wallet_repository, w3_service=w3_service)
