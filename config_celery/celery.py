from celery import Celery
from config.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "src.gateway.tasks",
        "config_celery.celery",
    ]
)
