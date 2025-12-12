from fastapi import APIRouter, Query
from typing import Optional

from app.modules.auth.roles.service import RoleService
from app.schemas.auth import CreateRole, UpdateRole

router = APIRouter()


@router.get("check")
async def check_role(name=Query(...)):
    service = RoleService()
    return await service.check_name(name)


@router.get("")
async def get_roles(name: Optional[str] = None, is_active: Optional[bool] = None):
    service = RoleService()
    return await service.get(name, is_active)


@router.post("")
async def create_role(data: CreateRole):
    service = RoleService()
    return await service.create(data.name, data.description, data.is_active)


@router.put("")
async def update_role(data: UpdateRole):
    service = RoleService()
    return await service.update(data.id, data.name, data.description, data.is_active)
