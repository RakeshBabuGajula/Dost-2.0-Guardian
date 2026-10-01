import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import settings

logger = logging.getLogger("dost_guardian.health")


def check_db_connection(db: Session) -> bool:
    try:
        db.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Health check DB ping failed: {e}")
        return False


def check_redis_connection(redis_client=None) -> bool:
    if not redis_client:
        return True  # Soft check if Redis optional in dev
    try:
        return redis_client.ping()
    except Exception as e:
        logger.warning(f"Health check Redis ping failed: {e}")
        return False
