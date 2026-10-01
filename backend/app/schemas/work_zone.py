from pydantic import BaseModel, ConfigDict


class WorkZoneBase(BaseModel):
    id: str
    name: str
    blockSectionCode: str
    startX: float
    endX: float
    bufferZoneMeters: float
    safetyZoneMeters: float
    assignedTeamCode: str


class WorkZoneResponse(WorkZoneBase):
    model_config = ConfigDict(from_attributes=True)
