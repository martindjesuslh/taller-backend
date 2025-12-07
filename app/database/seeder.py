from logging import getLogger

from app.config.database import db_manager
from app.database.query_manager import QueryManager
from app.database.seeder_query import (
    CREATE_SCHEMAS,
    CREATE_TABLES,
    CREATE_INDEXES,
    CREATE_FUNCTIONS,
    CREATE_TRIGGERS,
)

logger = getLogger(__name__)


async def run_seeder():
    logger.info("Starting database seeding...")

    all_queries = (
        CREATE_SCHEMAS
        + CREATE_TABLES
        + CREATE_INDEXES
        + CREATE_FUNCTIONS
        + CREATE_TRIGGERS
    )

    async with db_manager.get_transaction() as conn:
        query_manager = QueryManager(conn)

        for i, query in enumerate(all_queries, 1):
            logger.info(f"Executing query {i}...")
            result = await query_manager.write(query)

            if not result.success:
                logger.error(f"Query {i} failed: {result.error}")
                raise Exception(f"Query {i} failed: {result.error}")
            logger.info(f"Query {i} executed successfully")

    logger.info("Database seeding completed successfully")
