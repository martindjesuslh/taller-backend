from typing import List, Dict, Any, Optional
from logging import getLogger
from fastapi import HTTPException,Response

from app.database.query_manager import QueryManager, QueryResult
from app.schemas.responses import ApiResponse, from_status

logger = getLogger(__name__)


class RoleService:
    def __init__(self):
        self.qm = QueryManager()

    async def create(
        self, name: str, description: Optional[str], is_active: bool
    ) -> QueryResult:
        query = """
            INSERT INTO "user".roles (name, description, is_active)
            VALUES ($1, $2, $3)
            RETURNING id, name, description, is_active
        """
        params = (name, description, is_active)

        response = await self.qm.write(query, params, True)

        if not response.success:
            raise from_status(
                response.status_code, response.message, error_message=response.error
            )

        return ApiResponse.created("Role created successfully", response.data)
