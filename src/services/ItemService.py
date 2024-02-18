from typing import Sequence

from fastapi import Depends, HTTPException
from starlette import status

from src.models.ItemModel import Item
from src.repositories.ItemRepository import ItemRepository
from src.schemas.ItemSchema import ItemSchemaCreate, ItemSchemaUpdate


class ItemService:
    def __init__(self, repo: ItemRepository = Depends()):
        self.repo = repo

    async def list(self) -> Sequence[Item]:
        return await self.repo.list()

    async def get(self, _id: int) -> Item:
        obj = await self.repo.get(_id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found",
            )
        return obj

    async def create(self, new_item: ItemSchemaCreate) -> Item:
        return await self.repo.create(new_item)

    async def update(self, _id: int, update_item: ItemSchemaUpdate) -> Item:
        old_obj = await self.get(_id)
        return await self.repo.update(old_obj, update_item)

    async def delete(self, _id: int) -> Item:
        return await self.repo.delete(_id)
