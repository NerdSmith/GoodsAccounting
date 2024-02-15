from sqlmodel import SQLModel, Field

from src.models.BaseIDModel import BaseIDModel


class PlaceBase(SQLModel):
    name: str = Field(index=True)
    max_weight: float


class PlaceDB(PlaceBase, BaseIDModel, table=True):
    pass
