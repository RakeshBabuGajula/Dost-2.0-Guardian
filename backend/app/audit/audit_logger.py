import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.domain_models import AuditLog


def log_audit_event(
    db: Session,
    actor: str,
    action: str,
    target: str,
    event_id: Optional[str] = None,
    request_id: Optional[str] = None,
    correlation_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> AuditLog:
    if not event_id:
        event_id = str(uuid.uuid4())

    audit_entry = AuditLog(
        id=str(uuid.uuid4()),
        event_id=event_id,
        actor=actor,
        action=action,
        target=target,
        timestamp=datetime.utcnow(),
        request_id=request_id,
        correlation_id=correlation_id,
        details=details or {},
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)
    return audit_entry
