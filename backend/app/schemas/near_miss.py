from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict


class NearMissBase(BaseModel):
    id: str
    occurredAt: str
    trainId: str
    trainSpeedKmh: float
    workerId: str
    workerName: str
    blockSectionCode: str
    minSpatialClearanceMeters: float
    ttdAtAckSeconds: int
    severity: str
    contributingFactors: List[str]
    locationCoords: Dict[str, float]


class NearMissResponse(NearMissBase):
    model_config = ConfigDict(from_attributes=True)
