from fastapi import APIRouter

from src.api.routes.channel import channel_router
from src.api.routes.start import start_router

api_router = APIRouter()
api_router.include_router(channel_router)
api_router.include_router(start_router)

