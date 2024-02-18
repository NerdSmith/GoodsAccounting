from fastapi import FastAPI

from src.api.v1.api import api_router as api_router_v1

app = FastAPI()

app.include_router(api_router_v1)
