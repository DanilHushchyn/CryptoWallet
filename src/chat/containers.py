from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.boto3.boto3_service import BotoService
from src.gateway.containers import DatabaseContainer
from src.chat.repository import ChatRepository
from src.chat.services.chat import ChatService


class ChatContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    chat_repository = providers.Factory(ChatRepository, session_factory=DatabaseContainer.session)
    boto3_service = providers.Factory(BotoService)
    chat_service = providers.Factory(ChatService, chat_repository=chat_repository, boto3_service=boto3_service)
