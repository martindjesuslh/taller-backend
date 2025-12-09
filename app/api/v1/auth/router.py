from fastapi import APIRouter, status
from .handler import create_role_handler
from app.schemas.auth import CreateRole

auth_router = APIRouter(prefix="/auth", tags=["roles"])


@auth_router.post("")
async def create_role(data: CreateRole):
    return await create_role_handler(data)
