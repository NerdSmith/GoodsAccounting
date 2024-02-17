from src.models.UserModel import UserBase


class CreateUserSchema(UserBase):
    password: str


class OutUserSchema(UserBase):
    id: int
