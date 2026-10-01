from typing import Optional
from pydantic import BaseModel, ConfigDict


class TrainBase(BaseModel):
    id: str
    number: str
    name: str
    line: str
    currentBlockSection: str
    positionX: float
    speedKmh: float
    direction: str
    status: str


class TrainResponse(TrainBase):
    model_config = ConfigDict(from_attributes=True)


class TrainPositionUpdate(BaseModel):
    train_id: str
    position_x: float
    speed_kmh: float
    current_block_section: Optional[str] = None
