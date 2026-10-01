import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.simulation_service import RailwayDigitalTwinSimulator

logger = logging.getLogger("dost_guardian.api.simulation")

router = APIRouter(prefix="/simulation", tags=["Railway Digital Twin Simulation"])


@router.post("/tick", response_model=Dict[str, Any])
async def advance_simulation_tick(
    speed_multiplier: float = Query(1.0, ge=0.1, le=10.0),
    db: Session = Depends(get_db),
):
    """
    Advances the Railway Digital Twin deterministic simulation by one step.
    Updates train position, evaluates SafetyEngine rules, and broadcasts WebSocket updates.
    """
    return await RailwayDigitalTwinSimulator.process_simulation_tick(db, speed_multiplier)
