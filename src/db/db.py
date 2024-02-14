import os
from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", default="sqlite+aiosqlite:///database.db")

async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )  # type: ignore
    async with async_session() as session:
        yield session
