from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db import get_async_session
from src.models.ItemModel import Item, ItemBase
from src.repositories.CrudRepository import CrudRepository


class ItemRepository(CrudRepository[Item, ItemBase, ItemBase]):
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        super().__init__(Item, db)
