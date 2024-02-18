from typing import Sequence

from fastapi import Depends, HTTPException
from starlette import status

from src.models.ItemModel import Item  # noqa: F401
from src.models.PlaceModel import Place

from src.repositories.PlaceRepository import PlaceRepository
from src.schemas.PlaceSchema import PlaceSchemaCreate, PlaceSchemaUpdate


class PlaceService:
    def __init__(self, repo: PlaceRepository = Depends()):
        self.repo = repo

    async def list(self) -> Sequence[Place]:
        return await self.repo.list()

    async def get(self, _id: int) -> Place:
        obj = await self.repo.get(_id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found",
            )
        return obj

    async def create(self, new_place: PlaceSchemaCreate) -> Place:
        return await self.repo.create(new_place)

    async def update(self, _id: int, update_place: PlaceSchemaUpdate) -> Place:
        old_obj = await self.get(_id)
        return await self.repo.update(old_obj, update_place)

    async def delete(self, _id: int) -> Place:
        return await self.repo.delete(_id)
