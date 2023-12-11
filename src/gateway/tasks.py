from typing import List

from asgiref.sync import async_to_sync
from fastapi_mail import MessageSchema, MessageType, FastMail
from pydantic import BaseModel, EmailStr

from config.settings import mail_conf
from config_celery.celery import celery_app


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
