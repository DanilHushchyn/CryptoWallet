import passlib.hash
from dependency_injector import containers, providers

from config.settings import WIRING_CONFIG
from src.gateway.db import Database
from src.gateway.repository import UserRepository, AuthRepository
from src.gateway.services.auth import AuthService
from src.gateway.services.users import UserService


class DatabaseContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    db = providers.Singleton(Database)
    session = providers.Callable(db.provided.session)


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    user_repository = providers.Factory(UserRepository, session_factory=DatabaseContainer.session)
    password_hasher = providers.Callable(passlib.hash.pbkdf2_sha256.hash)
    user_service = providers.Factory(UserService, user_repository=user_repository, hashed_psw=password_hasher.provider)


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=WIRING_CONFIG)
    auth_repository = providers.Factory(AuthRepository, session_factory=DatabaseContainer.session)
    password_hasher = providers.Callable(passlib.hash.pbkdf2_sha256.hash)
    auth_service = providers.Factory(AuthService, auth_repository=auth_repository, hashed_psw=password_hasher.provider)
