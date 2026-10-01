from typing import Optional
from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    id: str
    workerId: str
    workerName: str
    trainId: str
    trainName: str
    blockSectionCode: str
    state: str  # CAUTION, WARNING, CRITICAL, EMERGENCY, SAFE
    timeToDangerSeconds: int
    distanceToTrainMeters: float
    escalationTier: str  # WORKER_ACK, TIER_1_SUPERVISOR, TIER_3_CONTROL_ROOM
    createdAt: str
    isAcknowledged: bool
    acknowledgedAt: Optional[str] = None
    acknowledgedBy: Optional[str] = None
    requiredAction: str


class AlertResponse(AlertBase):
    model_config = ConfigDict(from_attributes=True)


class AlertAcknowledgeRequest(BaseModel):
    worker_id: str
    acknowledged_by: Optional[str] = "Worker"
    notes: Optional[str] = None
