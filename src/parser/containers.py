from dependency_injector import containers, providers
from config.settings import WIRING_CONFIG
from src.gateway.containers import DatabaseContainer
from src.parser.repository import ParserRepository
from src.parser.services.block_parser import ParserService
from src.web3.repository import WebRepository
from src.web3.web3_service import WebService


class ParserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    parser_repository = providers.Factory(ParserRepository, session_factory=DatabaseContainer.session)
    web3_repository = providers.Factory(WebRepository, session_factory=DatabaseContainer.session)
    w3_service = providers.Singleton(WebService, web3_repository=web3_repository)
    parser_service = providers.Factory(ParserService, parser_repository=parser_repository, w3_service=w3_service)