import socketio
from celery import Celery

from config_celery import celery
from config_celery.celery import celery_app
from config_socketio.app import sio
from src.gateway.register import RegisterContainer


def create_celery_app() -> Celery:
    container = RegisterContainer()
    celery_app.container = container
    return celery_app


celery_application = create_celery_app()