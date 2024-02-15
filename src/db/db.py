import asyncio
import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
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


async def init_db() -> None:
    from src.models.PlaceModel import Place  # noqa: F401
    from src.models.ItemModel import Item  # noqa: F401
    from src.models.UserModel import User  # noqa: F401

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
