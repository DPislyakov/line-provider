from fastapi import APIRouter
from .endpoints import (
    event as api_event,
)

api_router = APIRouter()
api_router.include_router(api_event.router, prefix='/event', tags=["Event"])
