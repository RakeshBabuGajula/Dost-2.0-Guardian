import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.domain_models import Alert, Worker
from app.audit.audit_logger import log_audit_event

logger = logging.getLogger("dost_guardian.alert_service")


def utc_now():
    return datetime.now(timezone.utc)


def format_alert_to_schema(alert: Alert) -> dict:
    return {
        "id": alert.id,
        "workerId": alert.worker_id,
        "workerName": alert.worker_name,
        "trainId": alert.train_id,
        "trainName": alert.train_name,
        "blockSectionCode": alert.block_section_code,
        "state": alert.state,
        "timeToDangerSeconds": alert.time_to_danger_seconds,
        "distanceToTrainMeters": alert.distance_to_train_meters,
        "escalationTier": alert.escalation_tier,
        "createdAt": alert.created_at.isoformat() if isinstance(alert.created_at, datetime) else str(alert.created_at),
        "isAcknowledged": alert.is_acknowledged,
        "acknowledgedAt": alert.acknowledged_at.isoformat() if alert.acknowledged_at else None,
        "acknowledgedBy": alert.acknowledged_by,
        "requiredAction": alert.required_action,
    }


def get_all_alerts(db: Session) -> List[dict]:
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).all()
    return [format_alert_to_schema(a) for a in alerts]


def get_active_unacknowledged_alerts(db: Session) -> List[dict]:
    alerts = (
        db.query(Alert)
        .filter(Alert.is_acknowledged.is_(False))
        .order_by(Alert.created_at.desc())
        .all()
    )
    return [format_alert_to_schema(a) for a in alerts]


def create_or_update_alert(
    db: Session,
    worker_id: str,
    worker_name: str,
    train_id: str,
    train_name: str,
    block_section_code: str,
    state: str,
    time_to_danger_seconds: int,
    distance_to_train_meters: float,
    escalation_tier: str = "WORKER_ACK",
    required_action: str = "CLEAR TRACK IMMEDIATELY",
) -> Tuple[dict, bool]:
    """
    Idempotently creates or updates an active alert for worker & train.
    Prevents duplicate active alerts for the same worker.
    Returns: (alert_dict, is_newly_created).
    """
    # Check existing unacknowledged alert for this worker
    existing = (
        db.query(Alert)
        .filter(Alert.worker_id == worker_id)
        .filter(Alert.is_acknowledged.is_(False))
        .first()
    )

    if existing:
        # Update existing alert telemetry
        existing.state = state
        existing.time_to_danger_seconds = time_to_danger_seconds
        existing.distance_to_train_meters = distance_to_train_meters
        existing.escalation_tier = escalation_tier
        existing.required_action = required_action
        existing.updated_at = utc_now()
        db.commit()
        db.refresh(existing)
        return format_alert_to_schema(existing), False

    # Create new alert
    alert_id = f"ALT-{int(utc_now().timestamp())}"
    alert = Alert(
        id=alert_id,
        worker_id=worker_id,
        worker_name=worker_name,
        train_id=train_id,
        train_name=train_name,
        block_section_code=block_section_code,
        state=state,
        time_to_danger_seconds=time_to_danger_seconds,
        distance_to_train_meters=distance_to_train_meters,
        escalation_tier=escalation_tier,
        required_action=required_action,
        is_acknowledged=False,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    db.add(alert)

    # Link alert to worker
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if worker:
        worker.status = state
        worker.unacknowledged_alert_id = alert_id

    db.commit()
    db.refresh(alert)

    log_audit_event(
        db=db,
        actor="SYSTEM_SAFETY_ENGINE",
        action="ALERT_CREATED",
        target=f"alert:{alert_id}",
        details={
            "worker_id": worker_id,
            "state": state,
            "ttd_seconds": time_to_danger_seconds,
            "distance": distance_to_train_meters,
        },
    )

    return format_alert_to_schema(alert), True


def acknowledge_alert(
    db: Session,
    alert_id: str,
    worker_id: str,
    acknowledged_by: str = "Worker",
) -> Optional[dict]:
    """
    Acknowledges an alert, updating worker status to SAFE.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        return None

    alert.is_acknowledged = True
    alert.acknowledged_at = utc_now()
    alert.acknowledged_by = acknowledged_by
    alert.state = "SAFE"

    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if worker:
        worker.status = "SAFE"
        worker.unacknowledged_alert_id = None

    db.commit()
    db.refresh(alert)

    log_audit_event(
        db=db,
        actor=acknowledged_by,
        action="ALERT_ACKNOWLEDGED",
        target=f"alert:{alert_id}",
        details={"worker_id": worker_id, "alert_id": alert_id},
    )

    return format_alert_to_schema(alert)


def escalate_alert(
    db: Session,
    alert_id: str,
    target_tier: str,
    reason: str = "Unacknowledged timeout",
) -> Optional[dict]:
    """
    Escalates an unacknowledged alert to Supervisor or Control Room tier.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert or alert.is_acknowledged:
        return None

    alert.escalation_tier = target_tier
    alert.updated_at = utc_now()
    db.commit()
    db.refresh(alert)

    log_audit_event(
        db=db,
        actor="SYSTEM_SAFETY_ENGINE",
        action="ALERT_ESCALATED",
        target=f"alert:{alert_id}",
        details={"target_tier": target_tier, "reason": reason},
    )
    return format_alert_to_schema(alert)
