from typing import Callable

import jwt

from config.settings import JWT_SECRET, ALGORITHM
from src.gateway.repository import AuthRepository


class AuthService:

    def __init__(self, auth_repository: AuthRepository, hashed_psw: Callable[[str], str]) -> None:
        self._repository: AuthRepository = auth_repository
        self.hashed_psw = hashed_psw

    async def get_auth(self, request):
        if request.cookies.get('access_token'):
            jwt_string = request.cookies.get('access_token')
            jwt_token = jwt_string.split(" ")[1]
            verify = jwt.decode(jwt_token, JWT_SECRET, leeway=10, algorithms=[ALGORITHM])
            if verify.get('id'):
                return True
        return False

    async def token(self, user):
        return await self._repository.token(user)

    async def register_user(self, user):
        user_model = user
        hashed_psw = self.hashed_psw(user.password)
        user_model.password = hashed_psw
        return await self._repository.add(user_model)

    async def chat_access(self, user_id):
        await self._repository.get_access(user_id=user_id)
