from typing import Union

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db import get_async_session
from src.models.UserModel import User, UserBase
from src.repositories.CrudRepository import CrudRepository, CreateSchemaType, ModelType


class UserRepository(CrudRepository[User, UserBase, UserBase]):
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        super().__init__(User, db)

    async def create(self, obj_in: Union[CreateSchemaType, ModelType]) -> ModelType:
        raise NotImplementedError
