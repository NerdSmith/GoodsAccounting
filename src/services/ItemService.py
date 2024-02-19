from typing import Sequence

from fastapi import Depends, HTTPException
from starlette import status

from src.models.ItemModel import Item
from src.repositories.ItemRepository import ItemRepository
from src.schemas.ItemSchema import ItemSchemaCreate, ItemSchemaUpdate
from src.services.PlaceService import PlaceService


class ItemService:
    def __init__(
        self, repo: ItemRepository = Depends(), place_service: PlaceService = Depends()
    ):
        self.repo = repo
        self.place_service = place_service

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
        target_place_id = new_item.place_id
        if target_place_id is not None:
            place = await self.place_service.get_with_weight(target_place_id)
            if place.current_weight + new_item.weight > place.max_weight:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="New object is too heavy",
                )
        return await self.repo.create(new_item)

    async def update(self, _id: int, update_item: ItemSchemaUpdate) -> Item:
        old_obj = await self.get(_id)
        if update_item.place_id is None:
            return await self.repo.update(old_obj, update_item)

        place_to = await self.place_service.get_with_weight(update_item.place_id)

        if (old_obj.place_id is None) or (
            old_obj.place_id != update_item.place_id
        ):  # change place
            if place_to.current_weight + update_item.weight > place_to.max_weight:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="New object is too heavy",
                )
        else:  # same place
            if (
                place_to.current_weight - old_obj.weight + update_item.weight
                > place_to.max_weight
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="New object is too heavy",
                )

        return await self.repo.update(old_obj, update_item)

    async def delete(self, _id: int) -> Item:
        return await self.repo.delete(_id)
