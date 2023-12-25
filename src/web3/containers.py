from dependency_injector import containers, providers

from config.settings import WIRING_CONFIG
from src.gateway.containers import DatabaseContainer
from src.web3.repository import WebRepository
from src.web3.web3_service import WebService


class Web3Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    web3_repository = providers.Factory(WebRepository, session_factory=DatabaseContainer.session)
    web3_service = providers.Factory(WebService, web3_repository=web3_repository)
