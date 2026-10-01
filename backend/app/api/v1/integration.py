import uuid
from typing import Dict, Any
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.integration_service import IntegrationAdapterService
from app.schemas.integration import (
    TrainPositionIngest, BlockStatusIngest, WorkOrderIngest, EmergencyIngest, NormalizedIntegrationResult
)
from app.security.auth import get_current_active_user
from app.models.domain_models import User

router = APIRouter(prefix="/integration", tags=["Authorized Railway Integration Adapter"])

def get_correlation_id(x_correlation_id: str = Header(None), x_request_id: str = Header(None)) -> str:
    return x_correlation_id or x_request_id or f"corr-{uuid.uuid4().hex[:8]}"

@router.post("/train-positions", response_model=NormalizedIntegrationResult)
def ingest_train_position(
    payload: TrainPositionIngest,
    correlation_id: str = Depends(get_correlation_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Ingest & normalize external train position telemetry into canonical WGS84 PostGIS geometry.
    Safety Boundary: Authorized integration boundary only. Does not connect to live signalling.
    """
    adapter = IntegrationAdapterService(db)
    return adapter.process_train_position_ingest(payload, correlation_id)

@router.post("/block-status", response_model=NormalizedIntegrationResult)
def ingest_block_status(
    payload: BlockStatusIngest,
    correlation_id: str = Depends(get_correlation_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Ingest & normalize external block section status update."""
    adapter = IntegrationAdapterService(db)
    return adapter.process_block_status_ingest(payload, correlation_id)

@router.post("/work-orders", response_model=NormalizedIntegrationResult)
def ingest_work_order(
    payload: WorkOrderIngest,
    correlation_id: str = Depends(get_correlation_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Ingest & normalize external maintenance work zone order."""
    adapter = IntegrationAdapterService(db)
    return adapter.process_work_order_ingest(payload, correlation_id)

@router.post("/emergencies", response_model=NormalizedIntegrationResult)
def ingest_emergency_event(
    payload: EmergencyIngest,
    correlation_id: str = Depends(get_correlation_id),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Ingest external track emergency notification."""
    adapter = IntegrationAdapterService(db)
    return adapter.process_emergency_ingest(payload, correlation_id)

@router.get("/contracts")
def get_integration_contracts() -> Dict[str, Any]:
    """Returns documentation of canonical integration schemas, versioning, and safety boundary policy."""
    return {
        "version": "v1.0-authorized-adapter",
        "coordinate_system": "WGS84 / EPSG:4326",
        "units": {"speed": "km/h", "distance": "meters", "heading": "degrees (0-360)"},
        "supported_ingests": [
            "TrainPositionIngest", "BlockStatusIngest", "WorkOrderIngest", "EmergencyIngest"
        ],
        "safety_policy": "AUTHORIZED-INTEGRATION-READY. System is not connected to live railway signalling or interlocking authority.",
        "authentication_requirement": "Bearer JWT token with CONTROL_ROOM, SUPERVISOR, or ADMIN role."
    }

@router.post("/simulate-tick")
def simulate_external_provider_tick(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Dict[str, Any]:
    """Runs a simulated external railway data provider tick for integration testing."""
    adapter = IntegrationAdapterService(db)
    return adapter.run_simulated_external_provider_tick()
