from fastapi import Depends

from src.models.UserModel import User
from src.repositories.UserRepository import UserRepository
from src.schemas.UserSchema import CreateUserSchema


class UserService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo

    async def create(self, new_user: CreateUserSchema) -> User:
        return await self.repo.create_with_password(new_user)
