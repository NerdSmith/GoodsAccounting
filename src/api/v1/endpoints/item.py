from typing import Sequence

from fastapi import APIRouter, Depends
from starlette import status

from src.schemas.ItemSchema import ItemSchema, ItemSchemaCreate, ItemSchemaUpdate
from src.services.ItemService import ItemService


router = APIRouter(prefix="/items")


@router.get("", response_model=Sequence[ItemSchema])
async def get_all_items(place_service: ItemService = Depends()):
    return await place_service.list()


@router.get("/{item_id}", response_model=ItemSchema)
async def get_item(item_id: int, item_service: ItemService = Depends()):
    return await item_service.get(item_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ItemSchema)
async def create_item(
    new_item: ItemSchemaCreate, item_service: ItemService = Depends()
):
    return await item_service.create(new_item)


@router.patch("/{item_id}", response_model=ItemSchema)
async def update_item(
    item_id: int, new_item: ItemSchemaUpdate, item_service: ItemService = Depends()
):
    return await item_service.update(item_id, new_item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, item_service: ItemService = Depends()):
    return await item_service.delete(item_id)
