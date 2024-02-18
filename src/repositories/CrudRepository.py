from typing import Generic, TypeVar, Sequence, Optional, Union

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.BaseIDModel import BaseIDModel

ModelType = TypeVar("ModelType", bound=BaseIDModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType], db: AsyncSession) -> None:
        self.db = db
        self.model = model

    async def list(
        self, offset: int = 0, limit: int = 100, **filters
    ) -> Sequence[ModelType]:
        q = select(self.model).filter_by(**filters).offset(offset).limit(limit)
        response = await self.db.execute(q)
        return response.scalars().all()

    async def get(self, _id: int) -> Optional[ModelType]:
        q = select(self.model).where(self.model.id == _id)
        response = await self.db.execute(q)
        return response.scalar_one_or_none()

    async def create(self, obj_in: Union[CreateSchemaType, ModelType]) -> ModelType:
        db_obj = self.model.from_orm(obj_in)
        try:
            self.db.add(db_obj)
            await self.db.commit()
        except exc.IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource could not be created",
            )
        await self.db.refresh(db_obj)
        return db_obj

    async def update(
        self, obj_current: ModelType, obj_new: UpdateSchemaType
    ) -> ModelType:
        update_data = obj_new.dict(exclude_unset=True)
        for field in update_data:
            setattr(obj_current, field, update_data[field])

        try:
            self.db.add(obj_current)
            await self.db.commit()
        except exc.IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource could not be updated",
            )
        await self.db.refresh(obj_current)
        return obj_current

    async def delete(self, _id: int) -> ModelType:
        q = select(self.model).where(self.model.id == _id)
        response = await self.db.execute(q)
        obj = response.scalar_one()
        await self.db.delete(obj)
        await self.db.commit()
        return obj
