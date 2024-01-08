import asyncio
from typing import List

from asgiref.sync import async_to_sync
from dependency_injector.wiring import inject, Provide
from fastapi.params import Depends
from fastapi_mail import MessageSchema, MessageType, FastMail
from pydantic import BaseModel, EmailStr

from config.settings import mail_conf
from config_celery.celery import celery_app
from src.gateway.containers import AuthContainer
from src.gateway.repository import AuthRepository
from src.gateway.services.auth import AuthService


class EmailSchema(BaseModel):
    email: List[EmailStr]


@celery_app.task(name="mailing_task")
def mailing_task(email_address: str):
    html = """<p>Hi you have successfully registered on Crypto Wallet!</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email_address],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(mail_conf)
    async_to_sync(fm.send_message)(message)
    return 'FINISHED SUCCESSFULL'


@celery_app.task(name="chat_access_task")
@inject
def chat_access_task(user_id: int, auth_service: AuthService = Provide[AuthContainer.auth_service]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(auth_service.chat_access(user_id))
    return 'CHAT ACCESS ACCEPTED'
