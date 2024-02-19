import asyncio
import os
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", default="sqlite+aiosqlite:///database.db")

async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_async_scoped_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    scoped_factory = async_scoped_session(
        async_session,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()


async def init_db() -> None:
    get_async_session()
    from src.models.PlaceModel import Place  # noqa: F401
    from src.models.ItemModel import Item  # noqa: F401
    from src.models.UserModel import User  # noqa: F401

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
