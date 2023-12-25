import datetime
import json

from dependency_injector.wiring import inject, Provide, Container
from fastapi import APIRouter
from fastapi import Response
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_mail import FastMail, MessageType, MessageSchema
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy_utils import URLType
from fastapi import status
from starlette.responses import JSONResponse

from config.settings import mail_conf
from src.gateway.containers import UserContainer, AuthContainer
from src.gateway.db import Base
from src.gateway.dependencies.jwt_auth import CustomJWTAuth
from src.gateway.repository import NotFoundError, UserRepository
from src.gateway.schemas import UserProfile, RegisterUserModel, AuthUsers
from src.gateway.services.auth import AuthService
from src.gateway.services.users import UserService
from utils.auth_operations import get_user_from_bearer
from src.gateway.tasks import mailing_task


main_router = APIRouter()
user_auth = CustomJWTAuth()


# ENDPOINTS
@main_router.get("/users", tags=['users'], status_code=status.HTTP_200_OK)
@inject
async def get_all(
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
        bearer: HTTPAuthorizationCredentials = Depends(user_auth)
):
    return await user_service.get_users()


@main_router.get("/user/{user_id}", tags=['users'], status_code=status.HTTP_200_OK)
@inject
async def get_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
        bearer: HTTPAuthorizationCredentials = Depends(user_auth)
):
    try:
        return await user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@main_router.delete("/user/{user_id}", tags=['users'], status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_by_id(
        user_id: int,
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
        bearer: HTTPAuthorizationCredentials = Depends(user_auth)
):
    try:
        await user_service.delete_user_by_id(user_id)
    except NotFoundError:
        return Response(content='User not found', status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(content='User deleted successfully', status_code=status.HTTP_204_NO_CONTENT)


@main_router.put("/edit_profile", tags=['users'], status_code=status.HTTP_200_OK)
@inject
async def edit_profile(profile: UserProfile,
                       user_service: UserService = Depends(Provide[UserContainer.user_service]),
                       bearer: HTTPAuthorizationCredentials = Depends(user_auth)
                       ):
    user = await get_user_from_bearer(bearer)
    return await user_service.edit_profile(profile, user)


@main_router.get("/user_by_token", tags=['users'], status_code=status.HTTP_200_OK)
@inject
async def get_by_token(
        user_service: UserService = Depends(Provide[UserContainer.user_service]),
        bearer: HTTPAuthorizationCredentials = Depends(user_auth)
):
    user_id = await get_user_from_bearer(bearer)
    try:
        return await user_service.get_user_by_id(user_id)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@main_router.post("/login", tags=['auth'], status_code=status.HTTP_200_OK)
@inject
async def login(
        user: AuthUsers,
        auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])) -> str:
    token = await auth_service.token(user)
    data = {'access_token': token}
    response = JSONResponse(content=data)
    if not user.remember:
        expire_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=15)
        response.set_cookie(key="access_token", value=f'Bearer {token}',
                            expires=expire_time.strftime('%a, %d-%b-%Y %T GMT'))
    else:
        response.set_cookie(key="access_token", value=f'Bearer {token}', max_age=10_000_000_000)

    return response


@main_router.post("/logout", tags=['auth'], status_code=status.HTTP_200_OK)
@inject
async def log_out(
        bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.set_cookie("access_token", value="", max_age=0)
    return response


@main_router.post("/register", tags=['auth'], status_code=status.HTTP_201_CREATED)
@inject
async def registration(
        user: RegisterUserModel,
        auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])
):
    user = await auth_service.register_user(user)
    mailing_task.delay(email_address=user.email)
    return user
