from fastapi import APIRouter

from src.api.v1.endpoints.user import router as user_router
from src.api.v1.endpoints.auth import router as auth_router
from src.api.v1.endpoints.place import router as place_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router, tags=["user"])
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(place_router, tags=["place"])
