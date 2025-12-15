from logging import getLogger
from typing import Any, Dict, Optional, List, Tuple
import asyncpg

logger = getLogger(__name__)


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

    async def select(
        self, query: str, params: Optional[Tuple] = None
    ) -> List[Dict[str, Any]]:
        try:
            conn = await self._get_connection()

            result = (
                await conn.fetch(query, *params) if params else await conn.fetch(query)
            )

            return [dict(row) for row in result]

        finally:
            if conn:
                await self._release_connection(conn)

    async def write(
        self, query: str, params: Optional[Tuple] = None, returning: bool = False
    ) -> List[Dict[str, Any]]:
        conn = None
        try:
            conn = await self._get_connection()

            if returning:
                result = (
                    await conn.fetch(query, *params)
                    if params
                    else await conn.fetch(query)
                )

                return [dict(row) for row in result]

            else:
                result = (
                    await conn.execute(query, *params)
                    if params
                    else await conn.execute(query)
                )

                return []

        finally:
            if conn:
                await self._release_connection(conn)

    async def transaction(
        self, queries: List[str], params_list: List[Tuple], returning: bool = False
    ):
        if len(queries) != len(params_list):
            raise ValueError("The quantity of queries is different than params")

        all_data = []

        async with self._db_manager.get_transaction() as conn:
            try:
                for query, params in zip(queries, params_list):
                    if returning:
                        result = (
                            await conn.fetch(query, *params)
                            if params
                            else await conn.fetch(query)
                        )
                        data = [dict(row) for row in result]
                        all_data.extend(data)
                    else:
                        result = (
                            await conn.execute(query, *params)
                            if params
                            else await conn.execute(query)
                        )

                    returning if returning else []

            except Exception as e:
                logger.error(f"Transaction failed: Rolling back: {e}")
                raise

    async def bulk_execute(self, query: str, params_list: List[Tuple]):
        try:
            conn = await self._get_connection()
            await conn.executemany(query, params_list)

        except Exception as e:
            logger.error(f"Bulk operation failed: {e}")
            raise
        finally:
            if conn:
                await self._release_connection(conn)
