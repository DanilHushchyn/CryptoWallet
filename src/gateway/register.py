from dependency_injector import containers, providers

from config.settings import WIRING_CONFIG
from src.delivery.containers import DeliveryContainer
from src.gateway.containers import DatabaseContainer, UserContainer, AuthContainer
from src.ibay.containers import IbayContainer
from src.wallet.containers import WalletContainer
from src.web3.containers import Web3Container
from src.chat.containers import ChatContainer


class RegisterContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    db_container = providers.Container(DatabaseContainer)
    users_container = providers.Container(UserContainer)
    auth_container = providers.Container(AuthContainer)
    wallet_container = providers.Container(WalletContainer)
    chat_container = providers.Container(ChatContainer)
    web3_container = providers.Container(Web3Container)
    ibay_container = providers.Container(IbayContainer)
    delivery_container = providers.Container(DeliveryContainer)
