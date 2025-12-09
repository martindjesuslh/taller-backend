from logging import getLogger
from fastapi import status
from fastapi.responses import JSONResponse

from app.schemas.auth import CreateRole
from app.modules.auth.roles.service import RoleService


async def create_role_handler(role_data: CreateRole):
    name = role_data.name
    description = role_data.description
    is_active = role_data.is_active

    service = RoleService()

    result = await service.create(name, description, is_active)

    return result
