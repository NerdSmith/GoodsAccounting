from typing import Sequence

from fastapi import APIRouter, Depends
from starlette import status

from src.schemas.PlaceSchema import PlaceSchema, PlaceSchemaCreate, PlaceSchemaUpdate

from src.services.PlaceService import PlaceService

router = APIRouter(prefix="/places")


@router.get("", response_model=Sequence[PlaceSchema])
async def get_all_places(place_service: PlaceService = Depends()):
    return await place_service.list()


@router.get("/{place_id}", response_model=PlaceSchema)
async def get_place(place_id: int, place_service: PlaceService = Depends()):
    return await place_service.get(place_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PlaceSchema)
async def create_place(
    new_place: PlaceSchemaCreate, place_service: PlaceService = Depends()
):
    return await place_service.create(new_place)


@router.patch("/{place_id}", response_model=PlaceSchema)
async def update_place(
    place_id: int, new_place: PlaceSchemaUpdate, place_service: PlaceService = Depends()
):
    return await place_service.update(place_id, new_place)


@router.delete(
    "/{place_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=PlaceSchema
)
async def delete_place(place_id: int, place_service: PlaceService = Depends()):
    return await place_service.delete(place_id)
