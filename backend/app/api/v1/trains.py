from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.train import TrainResponse, TrainPositionUpdate
from app.services.train_service import get_all_trains, get_train_by_id
from app.models.domain_models import Train
from app.realtime.connection_manager import connection_manager

router = APIRouter(prefix="/trains", tags=["Locomotive Telemetry & Trains"])


@router.get("", response_model=List[TrainResponse])
def list_trains(db: Session = Depends(get_db)):
    """Retrieve active train telemetry and positions across block sections."""
    return get_all_trains(db)


@router.get("/{train_id}", response_model=TrainResponse)
def get_train(train_id: str, db: Session = Depends(get_db)):
    """Retrieve specific train telemetry by ID."""
    train_data = get_train_by_id(db, train_id)
    if not train_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Train '{train_id}' not found",
        )
    return train_data


@router.post("/{train_id}/position", response_model=dict)
async def update_train_position(
    train_id: str,
    update: TrainPositionUpdate,
    db: Session = Depends(get_db),
):
    """Ingest synthetic train telemetry update."""
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Train '{train_id}' not found",
        )

    train.position_x = update.position_x
    train.speed_kmh = update.speed_kmh
    if update.current_block_section:
        train.current_block_section = update.current_block_section

    db.commit()

    event = {
        "event_id": f"evt-trn-{train_id}",
        "event_type": "TRAIN_POSITION_UPDATE",
        "entity_id": train_id,
        "occurred_at": train.updated_at.isoformat(),
        "payload": {
            "train_id": train_id,
            "position_x": update.position_x,
            "speed_kmh": update.speed_kmh,
        },
    }
    await connection_manager.broadcast(event)

    return {"status": "UPDATED", "train_id": train_id}
