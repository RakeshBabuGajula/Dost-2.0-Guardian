from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.common import HealthStatus
from app.health.checker import check_db_connection, check_redis_connection
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])

@router.get("/live", response_model=dict)
def health_liveness():
    """Liveness probe: returns 200 if FastAPI application process is running."""
    return {"status": "UP", "service": "dost-guardian-backend"}

@router.get("/ready", response_model=HealthStatus)
def health_readiness(db: Session = Depends(get_db)):
    """Readiness probe: verifies PostgreSQL and Redis dependencies."""
    db_ok = check_db_connection(db)
    redis_ok = check_redis_connection()

    if not db_ok:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable",
        )

    return HealthStatus(
        status="HEALTHY" if (db_ok and redis_ok) else "DEGRADED",
        app_alive=True,
        db_connected=db_ok,
        redis_connected=redis_ok,
    )

@router.get("/deep")
def health_deep_diagnostic(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Deep health diagnostic endpoint returning comprehensive component metrics."""
    metrics_svc = MetricsService(db)
    return metrics_svc.get_system_metrics()

@router.get("", response_model=HealthStatus)
def health_overall(db: Session = Depends(get_db)):
    """General health status diagnostic endpoint."""
    db_ok = check_db_connection(db)
    redis_ok = check_redis_connection()

    return HealthStatus(
        status="HEALTHY" if (db_ok and redis_ok) else "DEGRADED",
        app_alive=True,
        db_connected=db_ok,
        redis_connected=redis_ok,
    )
