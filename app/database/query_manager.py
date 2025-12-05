from logging import getLogger
from typing import Optional, Dict, Any, List, Tuple
import asyncpg

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
    def __init__(self, connection: Optional[asyncpg.Connection] = None):
        self._conn = connection
        self._owns_connection = connection is None

    @property
    def _db_manager(self):
        from app.config.database import db_manager

        return db_manager

    async def _get_connection(self) -> asyncpg.Connection:
        if self._conn:
            return self._conn

        if not self._db_manager.pool:
            raise RuntimeError(
                "Database pool not initialized. Call db_manager.connect() first."
            )

        return await self._db_manager.pool.acquire()

    async def _release_connection(self, conn: asyncpg.Connection):
        if self._owns_connection and self._db_manager.pool:
            await self._db_manager.pool.release(conn)

    async def select(self, query: str, params: Optional[Tuple] = None) -> QueryResult:
        try:
            conn = await self._get_connection()

            result = (
                await conn.fetch(query, *params) if params else await conn.fetch(query)
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

        finally:
            if conn:
                await self._release_connection(conn)

    async def write(
        self, query: str, params: Optional[Tuple] = None, returning: bool = False
    ) -> QueryResult:
        conn = None
        try:
            conn = await self._get_connection()

            if returning:
                result = (
                    await conn.fetch(query, *params)
                    if params
                    else await conn.fetch(query)
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
                    await conn.execute(query, *params)
                    if params
                    else await conn.execute(query)
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

        finally:
            if conn:
                await self._release_connection(conn)

    async def transaction(
        self, queries: List[str], params_list: List[Tuple], returning: bool = False
    ):
        if len(queries) != len(params_list):
            return QueryResult(
                success=False,
                data=[],
                message="Transition failed",
                error="The quantity of queries is different than params",
            )

        all_data = []
        total_affected = 0

        async with self._db_manager.get_transaction() as conn:
            try:
                for i, (query, params) in enumerate(zip(queries, params_list)):
                    if returning:
                        result = (
                            await conn.fetch(query, *params)
                            if params
                            else await conn.fetch(query)
                        )
                        data = [dict(row) for row in result]
                        all_data.extend(data)
                        total_affected += len(data)
                    else:
                        result = (
                            await conn.fetch(query, *params)
                            if params
                            else await conn.fetch(query)
                        )
                        if " " in result and result.split()[-1].isdigit():
                            total_affected += int(result.split()[-1])

                    logger.debug(f"Query {i + 1}/{len(queries)} executed successfully")

                return QueryResult(
                    success=True,
                    data=all_data if returning else [],
                    message=f"Transaction completed: {len(queries)} queries executed",
                    affected_rows=total_affected,
                )

            except Exception as e:
                logger.error(f"Transaction failed: {e}")
                return QueryResult(
                    success=False,
                    data=[],
                    message="Transaction failed",
                    error=str(e),
                    affected_rows=total_affected,
                )

    async def bulk_execute(self, query: str, params_list: List[Tuple]) -> QueryResult:
        try:
            conn = await self._get_connection()

            await conn.executemany(query, params_list)
            affected_rows = len(params_list)

            return QueryResult(
                success=True,
                data=[],
                message=f"Batch operation completed, {affected_rows} operations executed",
                affected_rows=affected_rows,
            )
        except Exception as e:
            logger.error(f"Batch operation error {e}")
            return QueryResult(
                success=False, data=[], message="Batch operation failed", error=str(e)
            )
