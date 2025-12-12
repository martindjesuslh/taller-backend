from typing import Optional

from app.database.query_manager import QueryManager, QueryResult
from app.database.query_builder import QueryBuilder
from app.schemas.responses import ApiResponse, from_status


class RoleService:
    def __init__(self):
        self.qm = QueryManager()

    async def check_name(self, name):
        query = """
            SELECT 1 FROM "user".roles WHERE name = $1 LIMIT 1;
        """
        params = (name,)

        response = await self.qm.select(query, params)
        exists_register = bool(response.data)

        return (
            ApiResponse.no_content()
            if exists_register
            else ApiResponse.not_found("Role not found")
        )

    async def get(self, name, active):
        qb = QueryBuilder("user", "roles")
        qb.select().where(name=name, is_active=active)

        query, params = qb.build_select()

        response = await self.qm.select(query, params)
        exists_register = bool(response.data)

        return (
            ApiResponse.ok(data=response.data)
            if exists_register
            else ApiResponse.no_content("Not found")
        )

    async def create(self, name, description, is_active) -> QueryResult:
        qb = QueryBuilder("user", "roles")
        qb.insert(name=name, description=description, is_active=is_active)

        query, params = qb.build_insert(["id", "name", "description", "is_active"])
        response = await self.qm.write(query, params, True)

        if not response.success:
            raise from_status(
                response.status_code, response.message, error_message=response.error
            )

        return ApiResponse.created("Role created successfully", response.data)

    async def update(self, id, name, description, is_active):
        qb = QueryBuilder("user", "roles")
        qb.set(name=name, description=description, is_active=is_active)
        qb.where(id=id)

        query, params = qb.build_update()

        response = await self.qm.write(query, params)

        if not response.success:
            raise from_status(
                response.status_code, response.message, error_message=response.error
            )

        return ApiResponse.ok("Update role")
