from fastapi import APIRouter
from . import roles

auth_router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])

auth_router.include_router(roles.router, prefix="/roles", tags=["roles"])
