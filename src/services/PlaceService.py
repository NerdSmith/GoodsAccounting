from typing import Sequence

from fastapi import Depends, HTTPException
from starlette import status

from src.models.ItemModel import Item  # noqa: F401
from src.models.PlaceModel import Place

from src.repositories.PlaceRepository import PlaceRepository
from src.schemas.PlaceSchema import (
    PlaceSchemaCreate,
    PlaceSchemaUpdate,
    WeightedPlaceSchema,
)


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
        old_weight = await self.get_weight(old_obj)
        if update_place.max_weight < old_weight:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This edit is not allowed",
            )
        return await self.repo.update(old_obj, update_place)

    async def delete(self, _id: int) -> Place:
        return await self.repo.delete(_id)

    @staticmethod
    async def get_weight(place: Place) -> float:
        total_weight = 0.0
        for item in place.items:
            total_weight += item.weight
        return total_weight

    async def get_with_weight(self, _id: int) -> WeightedPlaceSchema:
        place = await self.get(_id)
        total_weight = await self.get_weight(place)
        weighted = WeightedPlaceSchema(
            **place.model_dump(exclude_unset=False), current_weight=total_weight
        )
        return weighted
