from dependency_injector.providers import Singleton
from contextlib import asynccontextmanager
import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from config.settings import URL

logger = logging.getLogger(__name__)

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "postgresql://danil:danil@localhost/crypto_wallet"


class Database(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.engine = create_async_engine(URL, echo=False, future=True)
        self._session_factory = async_sessionmaker(self.engine, autoflush=False, expire_on_commit=False)

    async def create_database(self) -> None:
        async with self.engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        async with self._session_factory() as _session:
            try:
                yield _session
            finally:
                await _session.close()


#
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
# from sqlalchemy.orm import sessionmaker
#
#
#
# # engine = create_engine(SQLALCHEMY_DATABASE_URL)
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
# Base: DeclarativeMeta = declarative_base()
