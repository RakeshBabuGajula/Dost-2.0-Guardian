from typing import Optional
from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    id: str
    workerId: Optional[str] = None
    deviceType: str
    firmwareVersion: str
    batteryPercentage: int
    networkSignalDbm: int
    lastPingAt: str
    status: str


class DeviceResponse(DeviceBase):
    model_config = ConfigDict(from_attributes=True)
