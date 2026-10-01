from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.alert import AlertResponse, AlertAcknowledgeRequest
from app.services.alert_service import get_all_alerts, acknowledge_alert, escalate_alert
from app.realtime.connection_manager import connection_manager

router = APIRouter(prefix="/alerts", tags=["Alerts & Escalation"])


@router.get("", response_model=List[AlertResponse])
def list_alerts(db: Session = Depends(get_db)):
    """Retrieve active and historical safety alerts."""
    return get_all_alerts(db)


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert_endpoint(
    alert_id: str,
    request: AlertAcknowledgeRequest,
    db: Session = Depends(get_db),
):
    """Acknowledge a critical or warning safety alert."""
    updated_alert = acknowledge_alert(
        db,
        alert_id=alert_id,
        worker_id=request.worker_id,
        acknowledged_by=request.acknowledged_by or "Worker",
    )
    if not updated_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert '{alert_id}' not found",
        )

    event = {
        "event_id": f"evt-ack-{alert_id}",
        "event_type": "ALERT_ACKNOWLEDGED",
        "entity_id": alert_id,
        "occurred_at": updated_alert["acknowledgedAt"],
        "payload": updated_alert,
    }
    await connection_manager.broadcast(event)

    return updated_alert


@router.post("/{alert_id}/escalate", response_model=AlertResponse)
async def escalate_alert_endpoint(
    alert_id: str,
    target_tier: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    """Escalate an unacknowledged alert to Supervisor or Control Room tier."""
    updated_alert = escalate_alert(db, alert_id=alert_id, target_tier=target_tier)
    if not updated_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert '{alert_id}' not found or already acknowledged",
        )

    event = {
        "event_id": f"evt-esc-{alert_id}",
        "event_type": "ALERT_ESCALATED",
        "entity_id": alert_id,
        "occurred_at": updated_alert.get("createdAt", ""),
        "payload": updated_alert,
    }
    await connection_manager.broadcast(event)

    return updated_alert
