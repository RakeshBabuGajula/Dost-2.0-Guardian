from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.worker import WorkerResponse, WorkerLocationUpdate
from app.services.worker_service import get_all_workers, get_worker_by_id
from app.models.domain_models import Worker
from app.realtime.connection_manager import connection_manager
from app.security.auth import get_current_user
from app.schemas.auth import UserInfo

router = APIRouter(prefix="/workers", tags=["Workers Roster & Safety"])


@router.get("", response_model=List[WorkerResponse])
def list_workers(db: Session = Depends(get_db)):
    """Retrieve operational roster of active gang maintainers and keymen."""
    return get_all_workers(db)


@router.get("/{worker_id}", response_model=WorkerResponse)
def get_worker(worker_id: str, db: Session = Depends(get_db)):
    """Retrieve detailed state and dynamic safety envelope for a specific worker."""
    worker_data = get_worker_by_id(db, worker_id)
    if not worker_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker '{worker_id}' not found",
        )
    return worker_data


@router.post("/{worker_id}/telemetry", response_model=dict)
async def update_worker_telemetry(
    worker_id: str,
    update: WorkerLocationUpdate,
    db: Session = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Ingest worker telemetry (GPS, battery, network status)."""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Worker '{worker_id}' not found",
        )

    worker.position_x = update.position_x
    worker.position_y = update.position_y
    worker.gps_accuracy_meters = update.gps_accuracy_meters
    if update.battery_level is not None:
        worker.battery_level = update.battery_level
    if update.network_state is not None:
        worker.network_state = update.network_state

    db.commit()

    # Broadcast real-time event via WebSocket
    event = {
        "event_id": f"evt-loc-{worker_id}",
        "event_type": "WORKER_LOCATION_UPDATE",
        "entity_id": worker_id,
        "occurred_at": worker.updated_at.isoformat(),
        "payload": {
            "worker_id": worker_id,
            "position_x": update.position_x,
            "position_y": update.position_y,
            "gps_accuracy": update.gps_accuracy_meters,
        },
    }
    await connection_manager.broadcast(event)

    return {"status": "UPDATED", "worker_id": worker_id}
