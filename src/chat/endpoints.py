from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status
from src.gateway.dependencies.jwt_auth import CustomJWTAuth
from src.chat.containers import ChatContainer
from src.chat.schemas import MessageForm, UserList
from src.chat.services.chat import ChatService
from utils.auth_operations import get_user_from_bearer

chat_router = APIRouter()

user_auth = CustomJWTAuth()


@chat_router.post("/send_message", tags=['chat'], status_code=status.HTTP_201_CREATED)
@inject
async def send_message(message: MessageForm, chat_service: ChatService = Depends(Provide[ChatContainer.chat_service]),
                       bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await chat_service.send_message(message, user_id)

@chat_router.get("/chat_access", tags=['chat'], status_code=status.HTTP_201_CREATED)
@inject
async def chat_access(chat_service: ChatService = Depends(Provide[ChatContainer.chat_service]),
                       bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await chat_service.chat_access(user_id)



@chat_router.get("/get_chat", tags=['chat'], status_code=status.HTTP_200_OK)
@inject
async def get_chat(chat_service: ChatService = Depends(Provide[ChatContainer.chat_service])):
    return await chat_service.get_chat()


@chat_router.get('/user_messages', tags=['chat'], status_code=status.HTTP_200_OK)
@inject
async def user_messages(chat_service: ChatService = Depends(Provide[ChatContainer.chat_service]),
                        bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    user_id = await get_user_from_bearer(bearer)
    return await chat_service.get_user_messages(user_id)


@chat_router.post('/online_users', tags=['chat'], status_code=status.HTTP_200_OK)
@inject
async def online_users(users_list: UserList, chat_service: ChatService = Depends(Provide[ChatContainer.chat_service]),
                        bearer: HTTPAuthorizationCredentials = Depends(user_auth)):
    return await chat_service.get_online_users(users_list.users)
