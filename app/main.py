from fastapi import FastAPI
from contextlib import asynccontextmanager
from logging import getLogger

from app.config.database import db_manager
from app.core.settings import settings
from app.database.seeder import run_seeder

from app.api.v1.main_router import api_router

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ADA Restauraciones API")

    try:
        logger.info("Initializing database connection pool...")
        await db_manager.connect()
        logger.info("Database pool connected")

        logger.info("Running database seeder...")
        await run_seeder()
        logger.info("Database seeding completed")

        logger.info("Performing database health check...")
        is_healthy = await db_manager.health_check()
        if is_healthy:
            logger.info("Database health check passed")
        else:
            logger.warning("Database health check failed")

        logger.info("Application startup completed successfully")

    except Exception as e:
        logger.error(f"APlication startup failed {e}")

        raise

    yield

    logger.info("Shutting down ADA Restauraciones")

    try:
        logger.info("Closing database connection pool...")
        await db_manager.disconnect()
        logger.info("Database pool disconnected")

    except Exception as e:
        logger.error(f"Error during shutdown {e}")

    logger.info("Application shutdown completed")


app = FastAPI(
    title="ADA Restauraciones API",
    description="API para gestión de taller de restauración de arte",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def read_root():
    """Endpoint raíz de bienvenida"""
    return {
        "message": "Bienvenido a ADA Restauraciones API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    db_healthy = await db_manager.health_check()

    return {"status": db_healthy}
