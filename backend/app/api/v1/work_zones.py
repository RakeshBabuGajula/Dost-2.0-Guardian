from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.work_zone import WorkZoneResponse
from app.models.domain_models import WorkZone

router = APIRouter(prefix="/work-zones", tags=["Work Zones & Geofencing"])


@router.get("", response_model=List[WorkZoneResponse])
def list_work_zones(db: Session = Depends(get_db)):
    """Retrieve active work zones and geofenced track boundaries."""
    work_zones = db.query(WorkZone).all()
    return [
        {
            "id": wz.id,
            "name": wz.name,
            "blockSectionCode": wz.block_section_code,
            "startX": wz.start_x,
            "endX": wz.end_x,
            "bufferZoneMeters": wz.buffer_zone_meters,
            "safetyZoneMeters": wz.safety_zone_meters,
            "assignedTeamCode": wz.assigned_team_code,
        }
        for wz in work_zones
    ]
