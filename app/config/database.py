from logging import getLogger
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import asyncpg
from fastapi import HTTPException, status

from app.core.settings import settings

logger = getLogger(__name__)


class DatabaseManager:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                database=settings.DB_NAME,
                command_timeout=60,
                min_size=1 if settings.ENVIRONMENT == "dev" else 5,
                max_size=5 if settings.ENVIRONMENT == "dev" else 20,
                max_queries=50000,
                max_inactive_connection_lifetime=300.0,  # 5 minutos
            )
            logger.info(
                f"Database connection pool initialized for {settings.ENVIRONMENT}"
            )

        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed",
            )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        if not self.pool:
            raise RuntimeError("Database not connected")

        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)

    @asynccontextmanager
    async def get_transaction(self) -> AsyncGenerator[asyncpg.Connection, None]:
        if not self.pool:
            raise RuntimeError("Database not connected")

        conn = await self.pool.acquire()
        trans = None
        try:
            trans = conn.transaction()
            await trans.start()
            yield conn
            await trans.commit()
            logger.info("Transaction committed successfully")
        except Exception as e:
            if trans:
                await trans.rollback()
                logger.error(f"Transaction rolled back due to error {e}")
            raise
        finally:
            await self.pool.release()

    async def health_check(self) -> bool:
        try:
            async with self.get_connection() as conn:
                await conn.fetchval("SELECT 1")
                return True
        except Exception:
            return False


db_manager: DatabaseManager = DatabaseManager()


async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    async for conn in db_manager.get_connection():
        yield conn


async def get_db_transition() -> AsyncGenerator[asyncpg.Connection, None]:
    async for conn in db_manager.get_transaction():
        yield conn
