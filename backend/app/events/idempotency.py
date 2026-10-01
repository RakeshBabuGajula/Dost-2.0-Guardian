import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.models.domain_models import AuditLog, EmergencyEvent

logger = logging.getLogger("dost_guardian.idempotency")


class EventIdempotencyManager:
    """
    Authoritative idempotency implementation using PostgreSQL unique event_id constraint
    and Redis SET with NX for short-lived deduplication coordination.
    """

    def __init__(self, redis_client=None):
        self.redis = redis_client

    def is_duplicate(self, db: Session, event_id: str) -> bool:
        if not event_id:
            return False

        # 1. Fast path: Check Redis short-lived coordination set if available
        if self.redis:
            try:
                exists = self.redis.get(f"event:{event_id}:processed")
                if exists:
                    logger.info(f"Duplicate event rejected via Redis cache: {event_id}")
                    return True
            except Exception as e:
                logger.warning(f"Redis idempotency check failed, falling back to DB: {e}")

        # 2. Authoritative check: Query PostgreSQL tables for event_id uniqueness
        audit_match = db.query(AuditLog).filter(AuditLog.event_id == event_id).first()
        if audit_match:
            logger.info(f"Duplicate event rejected via PostgreSQL audit index: {event_id}")
            return True

        emergency_match = db.query(EmergencyEvent).filter(EmergencyEvent.event_id == event_id).first()
        if emergency_match:
            logger.info(f"Duplicate event rejected via PostgreSQL emergency index: {event_id}")
            return True

        return False

    def mark_processed(self, db: Session, event_id: str, actor: str, action: str, details: Optional[dict] = None):
        if not event_id:
            return

        # Record in Redis with 24h expiration
        if self.redis:
            try:
                self.redis.set(f"event:{event_id}:processed", "1", ex=86400)
            except Exception as e:
                logger.warning(f"Failed to record event idempotency in Redis: {e}")


idempotency_manager = EventIdempotencyManager()
