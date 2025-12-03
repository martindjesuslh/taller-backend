from logging import getLogger
from typing import Optional, Dict, Any, List, Tuple
import asyncpg
from fastapi import HTTPException, status

from app.config.database import get_db_connection

logger = getLogger(__name__)


class QueryResult:
    def __init__(
        self,
        success: bool,
        data: List[Dict[str, Any]],
        message: Optional[str] = None,
        error: Optional[str] = None,
        affected_rows: int = 0,
    ):
        self.success = success
        self.data = data
        self.message = message
        self.error = error
        self.affected_rows = affected_rows

    def dict(self):
        return {
            "success": self.success,
            "data": self.data,
            "message": self.message,
            "error": self.error,
            "affected_rows": self.affected_rows,
        }


class QueryManager:
    def __init__(self, connection: asyncpg.Connection):
        self.conn: asyncpg.Connection = connection

    async def select(self, query: str, params: Optional[Tuple]) -> QueryResult:
        try:
            result = (
                await self.conn.fetch(query, *params)
                if params
                else await self.conn.fetch(query)
            )
            data = [dict(row) for row in result]

            return QueryResult(
                success=True,
                data=data,
                message=f"Retrieved {len(data)} records",
                affected_rows=len(data),
            )

        except Exception as e:
            logger.error(f"Query execution error: {e}")
            return QueryResult(
                success=False, data=[], message="Query execution failed", error=str(e)
            )

    async def write(
        self, query: str, params: Optional[Tuple] = None, returning: bool = False
    ) -> QueryResult:
        try:
            if returning:
                result = (
                    await self.conn.fetch(query, *params)
                    if params
                    else await self.conn.fetch(query)
                )

                data = [dict(row) for row in result]
                affected_rows = len(data)

                return QueryResult(
                    success=True,
                    data=data,
                    message=f"Write operation completed, {affected_rows} rows returned",
                    affected_rows=affected_rows,
                )
            else:
                result = (
                    await self.conn.execute(query, *params)
                    if params
                    else await self.conn.execute(query)
                )

                affected_rows = 0
                if " " in result and result.split()[-1].isdigit():
                    affected_rows = int(result.split()[-1])

                return QueryResult(
                    success=True,
                    data=[],
                    message="Write operation completed",
                    affected_rows=affected_rows,
                )

        except Exception as e:
            logger.error(f"Write operation error: {e}")
            return QueryResult(
                success=False, data=[], message="Write operation failed", error=str(e)
            )
