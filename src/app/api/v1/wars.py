from fastapi import APIRouter

from src.app.api.v1.endpoints import (
    example,
)

router = APIRouter()

router.include_router(example.router)
