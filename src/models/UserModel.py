from typing import Optional

from sqlmodel import SQLModel, Field

from .BaseIDModel import BaseIDModel


class UserBase(SQLModel):
    username: str


class User(UserBase, BaseIDModel, table=True):
    __tablename__ = "appuser"

    username: str = Field(unique=True)
    hashed_password: Optional[str] = Field(default=None, nullable=False)
