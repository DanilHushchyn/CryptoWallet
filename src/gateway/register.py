from dependency_injector import containers, providers

from config.settings import WIRING_CONFIG
from src.gateway.containers import DatabaseContainer, UserContainer, AuthContainer
from src.wallet.containers import WalletContainer
from src.web3.containers import Web3Container


class RegisterContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    db_container = providers.Container(DatabaseContainer)
    users_container = providers.Container(UserContainer)
    auth_container = providers.Container(AuthContainer)
    wallet_container = providers.Container(WalletContainer)
    web3_container = providers.Container(Web3Container)
