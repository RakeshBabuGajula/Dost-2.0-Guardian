from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.analytics_service import AnalyticsService
from app.security.auth import get_current_active_user, require_roles
from app.models.domain_models import User

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/kpis")
def get_operational_kpis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Fetch live operational KPIs for the Command Center."""
    service = AnalyticsService(db)
    return service.get_operational_kpis()

@router.get("/timeline")
def get_event_timeline(
    entity_type: Optional[str] = Query(None, description="WORKER, TRAIN, WORK_ZONE"),
    entity_id: Optional[str] = Query(None, description="ID of entity"),
    event_type: Optional[str] = Query(None, description="Event type filter"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[Dict[str, Any]]:
    """Fetch operational event timeline."""
    service = AnalyticsService(db)
    return service.get_event_timeline(entity_type=entity_type, entity_id=entity_id, event_type=event_type, limit=limit)

@router.get("/safety-metrics")
def get_safety_metrics(
    timeframe: str = Query("today", description="1h, today, 24h, 7d, 30d"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Fetch safety trend metrics and severity distribution."""
    service = AnalyticsService(db)
    return service.get_safety_metrics(timeframe=timeframe)

@router.get("/heatmap")
def get_safety_heatmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[Dict[str, Any]]:
    """Fetch spatial safety heatmap cluster points."""
    service = AnalyticsService(db)
    return service.get_safety_heatmap()

@router.get("/work-zones/{work_zone_id}")
def get_work_zone_profile(
    work_zone_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Fetch work zone operational profile."""
    service = AnalyticsService(db)
    profile = service.get_work_zone_profile(work_zone_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work Zone not found")
    return profile

@router.get("/teams/{team_id}")
def get_team_profile(
    team_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Fetch team operational safety profile."""
    service = AnalyticsService(db)
    profile = service.get_team_profile(team_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return profile
