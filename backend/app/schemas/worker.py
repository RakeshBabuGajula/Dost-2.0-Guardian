from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class WorkerPositionSchema(BaseModel):
    x: float
    y: float


class WorkerEnvelopeSchema(BaseModel):
    radiusMeters: float
    gpsUncertaintyBufferMeters: float
    trackGeometryBufferMeters: float
    isExpandedDueToGps: bool


class WorkerBase(BaseModel):
    id: str
    name: str
    role: str
    currentBlockSection: str
    status: str  # SAFE, CAUTION, WARNING, CRITICAL, EMERGENCY, DEGRADED_NETWORK
    networkState: str  # ONLINE, OFFLINE, DEGRADED
    batteryLevel: int
    gpsAccuracyMeters: float
    position: WorkerPositionSchema
    unacknowledgedAlertId: Optional[str] = None
    envelope: WorkerEnvelopeSchema


class WorkerCreate(BaseModel):
    id: str
    name: str
    role: str
    currentBlockSection: str
    teamId: Optional[str] = None


class WorkerResponse(WorkerBase):
    model_config = ConfigDict(from_attributes=True)


class WorkerLocationUpdate(BaseModel):
    worker_id: str
    position_x: float
    position_y: float
    gps_accuracy_meters: float
    battery_level: Optional[int] = None
    network_state: Optional[str] = None
