from typing import List

from sqlmodel import SQLModel, Field, Relationship

from .BaseIDModel import BaseIDModel


class PlaceBase(SQLModel):
    name: str = Field(index=True)
    max_weight: float


class Place(PlaceBase, BaseIDModel, table=True):
    items: List["Place"] = Relationship(back_populates="place")
