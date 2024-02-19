import asyncio
import os
from typing import Dict

from celery import Celery
from dotenv import load_dotenv

from src.repositories.PlaceRepository import PlaceRepository
from src.services.PlaceService import PlaceService
from src.utils.LayerUtils import get_service

load_dotenv()

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "amqp://admin:admin@localhost:5672"
)
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
)


async def get_weighted_place(place_id: int) -> Dict[str, str]:
    service = await get_service(PlaceService, PlaceRepository)

    weighted_item = await service.get_with_weight(_id=place_id)

    return weighted_item.model_dump()


@celery.task(name="calc_weight_of_items_on_place")  # type: ignore
def calc_weight_of_items_on_place(place_id: int) -> Dict[str, str]:
    weight = asyncio.run(get_weighted_place(place_id))
    return weight
