from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.TokenSchema import TokenSchema, TokenSchemaAccess, TokenSchemaRefresh
from src.services.AuthService import AuthService

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return await auth_service.login(form_data.username, form_data.password)


@router.post("/refresh", response_model=TokenSchemaAccess)
async def refresh(
    refresh_token: TokenSchemaRefresh, auth_service: AuthService = Depends()
):
    return await auth_service.get_access_by_refresh(refresh_token)
