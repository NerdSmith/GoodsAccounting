from typing import Optional

from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db import get_async_session
from src.models.UserModel import User
from src.repositories.CrudRepository import CrudRepository
from src.schemas.UserSchema import CreateUserSchema
from src.utils.PasswordUtils import get_hashed_password


class UserRepository(CrudRepository[User, CreateUserSchema, User]):
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        super().__init__(User, db)

    async def create_with_password(self, obj_in: CreateUserSchema) -> User:
        new_user = User(**obj_in.dict())
        hashed_password = get_hashed_password(obj_in.password)
        new_user.hashed_password = hashed_password
        new_user = await self.create(new_user)

        return new_user

    async def get_by_username(self, username: str) -> Optional[User]:
        q = select(self.model).where(self.model.username == username)
        response = await self.db.execute(q)
        return response.scalar_one_or_none()
