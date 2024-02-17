from fastapi import APIRouter, Depends
from starlette import status

from src.schemas.UserSchema import CreateUserSchema, OutUserSchema
from src.services.UserService import UserService

router = APIRouter(prefix="/user")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=OutUserSchema)
async def create_user(
    new_user: CreateUserSchema, user_service: UserService = Depends()
):
    return await user_service.create(new_user)
