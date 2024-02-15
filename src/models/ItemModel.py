from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .BaseIDModel import BaseIDModel
from .PlaceModel import Place


class ItemBase(SQLModel):
    name: str = Field(index=True)
    weight: float
    place_id: Optional[int] = Field(default=None, foreign_key="place.id")


class Item(ItemBase, BaseIDModel, table=True):
    place: Optional[Place] = Relationship(back_populates="items")
