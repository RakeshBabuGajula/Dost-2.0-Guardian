import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.domain_models import EmergencyEvent, Worker
from app.audit.audit_logger import log_audit_event

logger = logging.getLogger("dost_guardian.emergency_service")


def utc_now():
    return datetime.now(timezone.utc)


def format_emergency_to_schema(ev: EmergencyEvent) -> dict:
    return {
        "id": ev.id,
        "eventId": ev.event_id,
        "workerId": ev.worker_id,
        "blockSectionCode": ev.block_section_code,
        "triggerType": ev.trigger_type,
        "status": ev.status,
        "acknowledgedBy": ev.acknowledged_by,
        "createdAt": ev.created_at.isoformat() if isinstance(ev.created_at, datetime) else str(ev.created_at),
        "updatedAt": ev.updated_at.isoformat() if isinstance(ev.updated_at, datetime) else str(ev.updated_at),
    }


def trigger_emergency_sos(
    db: Session,
    worker_id: str,
    trigger_type: str = "MANUAL_SOS",
    block_section_code: str = "MAS-AJJ-DOWN-120",
) -> dict:
    """
    Triggers an emergency SOS event, sets worker status to EMERGENCY,
    and logs an authoritative audit event.
    """
    event_id = f"evt-sos-{worker_id}-{int(utc_now().timestamp())}"

    # Update worker safety status
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if worker:
        worker.status = "EMERGENCY"
        block_section_code = worker.current_block_section

    # Idempotency check: if active SOS exists for worker, reuse
    existing = (
        db.query(EmergencyEvent)
        .filter(EmergencyEvent.worker_id == worker_id)
        .filter(EmergencyEvent.status == "ACTIVE")
        .first()
    )
    if existing:
        return format_emergency_to_schema(existing)

    emergency_event = EmergencyEvent(
        event_id=event_id,
        worker_id=worker_id,
        block_section_code=block_section_code,
        trigger_type=trigger_type,
        status="ACTIVE",
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    db.add(emergency_event)
    db.commit()
    db.refresh(emergency_event)

    log_audit_event(
        db=db,
        actor=f"worker:{worker_id}",
        action="EMERGENCY_SOS_TRIGGERED",
        target=f"emergency:{event_id}",
        details={"worker_id": worker_id, "trigger_type": trigger_type, "block": block_section_code},
    )

    return format_emergency_to_schema(emergency_event)


def resolve_emergency(
    db: Session,
    event_id: str,
    resolved_by: str = "Control Room",
) -> Optional[dict]:
    """Resolves an active emergency event."""
    ev = db.query(EmergencyEvent).filter(EmergencyEvent.event_id == event_id).first()
    if not ev:
        return None

    ev.status = "RESOLVED"
    ev.acknowledged_by = resolved_by
    ev.updated_at = utc_now()

    worker = db.query(Worker).filter(Worker.id == ev.worker_id).first()
    if worker:
        worker.status = "SAFE"

    db.commit()
    db.refresh(ev)

    log_audit_event(
        db=db,
        actor=resolved_by,
        action="EMERGENCY_RESOLVED",
        target=f"emergency:{event_id}",
        details={"event_id": event_id, "worker_id": ev.worker_id},
    )

    return format_emergency_to_schema(ev)
