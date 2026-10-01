from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class TrainPositionIngest(BaseModel):
    train_id: str = Field(..., example="TRN-EXT-204")
    number: str = Field(..., example="12626")
    name: str = Field("MAS-SBC Express", example="MAS-SBC Express")
    line: str = Field("DOWN", example="DOWN")
    block_section_code: str = Field(..., example="MAS-AJJ-DOWN-120")
    latitude: float = Field(..., example=13.0827)
    longitude: float = Field(..., example=80.2707)
    speed_kmh: float = Field(..., ge=0.0, le=200.0, example=110.0)
    heading_degrees: float = Field(90.0, ge=0.0, le=360.0, example=90.0)
    direction: str = Field("EASTBOUND", example="EASTBOUND")
    source_system_id: str = Field(..., example="TMS-SOUTHERN-RAILWAY-V1")
    timestamp: str = Field(..., example="2026-09-30T20:00:00Z")

class BlockStatusIngest(BaseModel):
    block_section_code: str = Field(..., example="MAS-AJJ-DOWN-120")
    status: str = Field(..., example="ACTIVE")  # ACTIVE, MAINTENANCE, OCCUPIED, SUSPENDED
    line_type: str = Field("DOWN", example="DOWN")
    speed_limit_kmh: int = Field(110, ge=10, le=160)
    source_system_id: str = Field(..., example="AXLE-COUNTER-MAS-AJJ")
    timestamp: str = Field(..., example="2026-09-30T20:00:00Z")

class WorkOrderIngest(BaseModel):
    work_zone_id: str = Field(..., example="WZ-EXT-402")
    name: str = Field(..., example="Track Renewal Section MAS-AJJ")
    block_section_code: str = Field(..., example="MAS-AJJ-DOWN-120")
    assigned_team_code: str = Field(..., example="GANG-04")
    buffer_zone_meters: float = Field(500.0, ge=100.0)
    safety_zone_meters: float = Field(200.0, ge=50.0)
    source_system_id: str = Field(..., example="WORK-ORDER-MGMT-SYS")
    timestamp: str = Field(..., example="2026-09-30T20:00:00Z")

class EmergencyIngest(BaseModel):
    event_id: str = Field(..., example="EMG-EXT-9901")
    worker_id: str = Field(..., example="WRK-101")
    block_section_code: str = Field(..., example="MAS-AJJ-DOWN-120")
    trigger_type: str = Field("MANUAL_SOS", example="MANUAL_SOS")
    details: Optional[Dict[str, Any]] = None
    source_system_id: str = Field(..., example="HANDHELD-UNIT-BLE-MESH")
    timestamp: str = Field(..., example="2026-09-30T20:00:00Z")

class NormalizedIntegrationResult(BaseModel):
    correlation_id: str
    status: str  # ACCEPTED, DEGRADED, REJECTED
    entity_type: str
    entity_id: str
    warnings: List[str] = []
    normalized_data: Dict[str, Any]
    timestamp: str
