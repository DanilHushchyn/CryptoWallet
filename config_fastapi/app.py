import sqlalchemy
from fastapi import FastAPI
from propan import RabbitBroker
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, MetaData
from starlette.staticfiles import StaticFiles
from fastapi_mail import ConnectionConfig

from config.settings import RABBITMQ_URL, URL
from config_socketio.consumers import socketio_router
from config_socketio.socketio_app import socket_app
from src.chat.endpoints import chat_router
from src.chat.views import chat_views
from src.delivery.consumers import delivery_broker_router
from src.delivery.endpoints import delivery_router
from src.gateway import models
from src.gateway.register import RegisterContainer
from src.gateway.endpoints import main_router
from src.gateway.views import gateway_views
from src.ibay.endpoints import product_router
from src.ibay.views import ibay_views
from src.wallet.consumers import wallet_broker_router
from src.wallet.endpoints import wallet_router
from src.wallet.views import wallet_views

broker = RabbitBroker(RABBITMQ_URL)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    container = RegisterContainer()
    app = FastAPI(title='CryptoWallet',
                  description='CryptoWallet API',
                  version='1.0.1',
                  )
    app.container = container

    # ENDPOINTS
    app.include_router(main_router, prefix=API_PREFIX)
    app.include_router(wallet_router, prefix=API_PREFIX)
    app.include_router(chat_router, prefix=API_PREFIX)
    app.include_router(product_router, prefix=API_PREFIX, tags=['product'])
    app.include_router(delivery_router, prefix=API_PREFIX, tags=['delivery'])

    # VIEWS
    app.include_router(wallet_views)
    app.include_router(ibay_views)
    app.include_router(gateway_views)
    app.include_router(chat_views)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount("/socket.io", socket_app)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app


app = create_app()


@app.on_event('startup')
async def publish_smtp():
    app.broker = broker
    app.broker.include_router(wallet_broker_router)
    app.broker.include_router(delivery_broker_router)
    app.broker.include_router(socketio_router)
    await broker.start()


@app.on_event('shutdown')
async def publish_smtp():
    await broker.close()
