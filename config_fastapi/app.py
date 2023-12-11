import sqlalchemy
from fastapi import FastAPI
from propan import RabbitBroker
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, MetaData
from starlette.staticfiles import StaticFiles
from fastapi_mail import ConnectionConfig

from config.settings import RABBITMQ_URL, URL
from src.gateway import models
from src.gateway.register import RegisterContainer
from src.gateway.endpoints import main_router
from src.wallet.endpoints import wallet_router

broker = RabbitBroker(RABBITMQ_URL)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


def create_app() -> FastAPI:
    container = RegisterContainer()
    app = FastAPI(title='CryptoWallet',
                  description='CryptoWallet API',
                  version='1.0.1',
                  )
    app.container = container
    # engine = create_engine(URL)
    # models.Base.metadata.create_all(bind=engine)

    app.include_router(main_router)
    app.include_router(wallet_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.mount("/socket.io", socket_app)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app


app = create_app()


@app.on_event('startup')
async def publish_smtp():
    app.broker = broker
    await broker.start()


@app.on_event('shutdown')
async def publish_smtp():
    await broker.close()
