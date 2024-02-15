from sqlmodel import SQLModel, Field

from .BaseIDModel import BaseIDModel


class PlaceBase(SQLModel):
    name: str = Field(index=True)
    max_weight: float


class Place(PlaceBase, BaseIDModel, table=True):
    pass
