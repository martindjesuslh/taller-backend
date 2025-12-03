from fastapi import FastAPI
from contextlib import asynccontextmanager
from logging import getLogger

from app.api.v1.routers import users
from app.database.seeder import init_seeder

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running database initialization...")
    try:
        await init_seeder()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

    logger.info("Application startup complete")

    yield

    logger.info("Application shutdown")


app = FastAPI(title="ADA Restauraciones API", lifespan=lifespan)

app.include_router(users.router, prefix="/api/v1", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Bienvenido a ADA Restauraciones API"}
