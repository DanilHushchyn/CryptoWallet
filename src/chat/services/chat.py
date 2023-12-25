from fastapi import HTTPException
from src.chat.repository import ChatRepository
from src.chat.schemas import MessageForm


class ChatService:

    def __init__(self, chat_repository: ChatRepository) -> None:
        self._repository: ChatRepository = chat_repository

    async def get_online_users(self, users):
        return await self._repository.get_online_users(users)


    async def send_message(self, message: MessageForm, user_id):
        if message.text == '' and message.image == '':
            raise HTTPException(status_code=401,
                                detail='Message empty data.')
        if not message.image == '':
            pass
        return await self._repository.add(message, user_id)

    async def chat_access(self, user_id):
        return await self._repository.chat_access(user_id)

    async def get_chat(self):
        chat_list = await self._repository.get_chat_messages()
        return chat_list


    async def get_user_messages(self, user_id):
        return await self._repository.user_messages(user_id)