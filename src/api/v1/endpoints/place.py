from typing import Sequence

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from starlette import status

from src.schemas.PlaceSchema import (
    PlaceSchema,
    PlaceSchemaCreate,
    PlaceSchemaUpdate,
    WeightedPlaceSchema,
)
from src.schemas.TasksSchemas import TaskSchema, TaskResultWPlaceSchema

from src.services.PlaceService import PlaceService

from src.tasks.worker import calc_weight_of_items_on_place

router = APIRouter(prefix="/places")


@router.get("", response_model=Sequence[PlaceSchema])
async def get_all_places(place_service: PlaceService = Depends()):
    return await place_service.list()


@router.get("/{place_id}", response_model=PlaceSchema)
async def get_place(place_id: int, place_service: PlaceService = Depends()):
    return await place_service.get(place_id)


@router.get("/weighted/{place_id}", response_model=WeightedPlaceSchema)
async def get_weighted_place(place_id: int, place_service: PlaceService = Depends()):
    return await place_service.get_with_weight(place_id)


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


@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_place(place_id: int, place_service: PlaceService = Depends()):
    return await place_service.delete(place_id)


@router.post("/worker/weighted/{place_id}", status_code=201, response_model=TaskSchema)
def get_weighted_place_with_worker(place_id: int):
    task = calc_weight_of_items_on_place.delay(place_id)
    return TaskSchema(task_id=task.task_id)


@router.get("/worker/tasks/{task_id}", response_model=TaskResultWPlaceSchema)
def get_weighted_place_with_worker_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return TaskResultWPlaceSchema(**result)
