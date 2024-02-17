from fastapi import APIRouter

from src.api.v1.endpoints.user import router as user_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user_router, tags=["user"])
