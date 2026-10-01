import uuid
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain_models import EmergencyEvent, Worker, Alert
from app.events.idempotency import idempotency_manager
from app.audit.audit_logger import log_audit_event
from app.realtime.connection_manager import connection_manager

router = APIRouter(prefix="/emergency-events", tags=["Emergency Operations"])


@router.post("", response_model=Dict[str, Any])
async def trigger_emergency_event(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
):
    """
    Trigger manual SOS or system-wide emergency event.
    Idempotent event handling verified via event_id.
    """
    event_id = payload.get("event_id") or str(uuid.uuid4())
    worker_id = payload.get("worker_id", "WRK-101")
    trigger_type = payload.get("trigger_type", "MANUAL_SOS")

    if idempotency_manager.is_duplicate(db, event_id):
        return {"status": "DUPLICATE_IGNORED", "event_id": event_id}

    emergency = EmergencyEvent(
        id=str(uuid.uuid4()),
        event_id=event_id,
        worker_id=worker_id,
        block_section_code=payload.get("block_section_code", "MAS-AJJ-DOWN-120"),
        trigger_type=trigger_type,
        status="ACTIVE",
    )
    db.add(emergency)

    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if worker:
        worker.status = "EMERGENCY"

    db.commit()

    idempotency_manager.mark_processed(
        db, event_id=event_id, actor=f"worker:{worker_id}", action="EMERGENCY_TRIGGERED"
    )

    log_audit_event(
        db=db,
        actor=f"worker:{worker_id}",
        action="EMERGENCY_TRIGGERED",
        target=f"worker:{worker_id}",
        event_id=event_id,
        details=payload,
    )

    event_envelope = {
        "event_id": event_id,
        "event_type": "EMERGENCY_TRIGGERED",
        "entity_id": worker_id,
        "occurred_at": emergency.created_at.isoformat(),
        "payload": {
            "worker_id": worker_id,
            "trigger_type": trigger_type,
            "block_section": emergency.block_section_code,
        },
    }
    await connection_manager.broadcast(event_envelope)

    return {"status": "ACKNOWLEDGED", "event_id": event_id, "emergency_id": emergency.id}
