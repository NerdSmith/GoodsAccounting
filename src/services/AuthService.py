from fastapi import Depends, HTTPException
from starlette import status

from src.schemas.TokenSchema import TokenSchema, TokenSchemaRefresh, TokenSchemaAccess
from src.repositories.UserRepository import UserRepository
from src.utils.PasswordUtils import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh,
)


class AuthService:
    def __init__(self, repo: UserRepository = Depends()):
        self.repo = repo

    async def login(self, username: str, password: str) -> TokenSchema:
        user = await self.repo.get_by_username(username)
        if user is None or not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )

        hashed_password: str = user.hashed_password
        if not verify_password(password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password",
            )

        payload = {
            "access_token": create_access_token(user.username),
            "refresh_token": create_refresh_token(user.username),
        }

        return TokenSchema(**payload)

    @staticmethod
    async def get_access_by_refresh(
        refresh_token: TokenSchemaRefresh,
    ) -> TokenSchemaAccess:
        token_data = verify_refresh(refresh_token)
        payload = {"access_token": create_access_token(token_data.sub)}
        return TokenSchemaAccess(**payload)
