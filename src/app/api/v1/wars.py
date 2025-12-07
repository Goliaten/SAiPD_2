from fastapi import APIRouter

from src.app.api.v1.endpoints import (
    UserManagement,
)

router = APIRouter()

router.include_router(UserManagement.router)
