from logging import getLogger

from app.config.database import db_manager
from app.database.query_manager import QueryManager
from app.database.seeder_query import CREATE_SCHEMAS, CREATE_TABLES

logger = getLogger(__name__)


async def _run_seeder():
    schema_queries = CREATE_SCHEMAS
    table_queries = CREATE_TABLES

    all_queries = schema_queries + table_queries

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


async def init_seeder():
    logger.info("TEST FUNCTION")
    await db_manager.connect()

    try:
        await _run_seeder()
    except Exception as e:
        logger.error(f"Seeder failed: {e}")
        raise
    finally:
        await db_manager.disconnect()
