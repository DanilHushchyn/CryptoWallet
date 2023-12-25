from typing import Optional, List
from pydantic import BaseModel


class MessageForm(BaseModel):
    text: str = ""
    image: str = ""


class ChatForm(BaseModel):
    user_id: int
    text: str
    image: str = ""
    date: str
    username: str
    user_avatar: str


class UserList(BaseModel):
    users: List[int]
