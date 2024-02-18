from fastapi import APIRouter, Depends
from starlette import status

from src.models.UserModel import User
from src.schemas.UserSchema import CreateUserSchema, OutUserSchema
from src.services.UserService import UserService
from src.utils.AuthUtils import get_current_user

router = APIRouter(prefix="/users")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=OutUserSchema)
async def create_user(
    new_user: CreateUserSchema, user_service: UserService = Depends()
):
    return await user_service.create(new_user)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=OutUserSchema)
async def user_me(current_user: User = Depends(get_current_user)):
    return current_user
