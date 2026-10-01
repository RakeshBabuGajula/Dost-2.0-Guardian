from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.near_miss import NearMissResponse
from app.models.domain_models import NearMiss

router = APIRouter(prefix="/near-misses", tags=["Near-Miss Intelligence"])


@router.get("", response_model=List[NearMissResponse])
def list_near_misses(db: Session = Depends(get_db)):
    """Retrieve recorded near-miss incidents and spatial clearance breach events."""
    near_misses = db.query(NearMiss).all()
    return [
        {
            "id": nm.id,
            "occurredAt": nm.occurred_at.strftime("%Y-%m-%d %H:%M:%S"),
            "trainId": nm.train_id,
            "trainSpeedKmh": nm.train_speed_kmh,
            "workerId": nm.worker_id,
            "workerName": nm.worker_name,
            "blockSectionCode": nm.block_section_code,
            "minSpatialClearanceMeters": nm.min_spatial_clearance_meters,
            "ttdAtAckSeconds": nm.ttd_at_ack_seconds,
            "severity": nm.severity,
            "contributingFactors": nm.contributing_factors or [],
            "locationCoords": nm.location_coords or {"x": 450, "y": 140},
        }
        for nm in near_misses
    ]
