from typing import Optional

from sqlmodel import SQLModel, Field

from src.models.BaseIDModel import BaseIDModel


class UserBase(SQLModel):
    username: str


class UserDB(UserBase, BaseIDModel, table=True):
    hashed_password: Optional[str] = Field(default=None, nullable=False, index=True)
