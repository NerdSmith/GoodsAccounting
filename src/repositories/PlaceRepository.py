from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db import get_async_session
from src.models.PlaceModel import PlaceBase, Place
from src.repositories.CrudRepository import CrudRepository


class PlaceRepository(CrudRepository[Place, PlaceBase, PlaceBase]):
    def __init__(
            self,
            db: AsyncSession = Depends(get_async_session)
    ):
        super().__init__(Place, db)


