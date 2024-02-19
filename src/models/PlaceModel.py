from typing import List

from sqlmodel import SQLModel, Field, Relationship

from .BaseIDModel import BaseIDModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ItemModel import Item


class PlaceBase(SQLModel):
    name: str = Field(index=True)
    max_weight: float


class Place(PlaceBase, BaseIDModel, table=True):
    items: List["Item"] = Relationship(
        back_populates="place", sa_relationship_kwargs={"lazy": "selectin"}
    )
