from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class LocationPoint(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="WGS84 Latitude")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="WGS84 Longitude")


class SpatialWorkerResult(BaseModel):
    id: str
    name: str
    role: str
    team_id: Optional[str] = None
    status: str
    current_block_section: str
    distance_meters: float
    latitude: float
    longitude: float
    gps_accuracy_meters: float
    last_updated_at: str


class SpatialTrainResult(BaseModel):
    id: str
    number: str
    name: str
    line: str
    speed_kmh: float
    heading: float
    direction: str
    current_block_section: str
    distance_meters: float
    latitude: float
    longitude: float
    last_updated_at: str


class RefugeResult(BaseModel):
    id: str
    code: str
    name: str
    refuge_type: str
    capacity_persons: int
    distance_meters: float
    latitude: float
    longitude: float


class BlockContextResult(BaseModel):
    code: str
    name: str
    line_type: str
    speed_limit_kmh: int
    status: str
    candidate_blocks: List[str]
    is_ambiguous: bool


class TrackSegmentResult(BaseModel):
    id: str
    code: str
    name: str
    track_code: str
    direction: str
    chainage_start_km: float
    chainage_end_km: float
    speed_limit_kmh: int
    distance_meters: float


class SpatialWorkerContext(BaseModel):
    worker_id: str
    worker_name: str
    current_location: LocationPoint
    containing_block: Optional[BlockContextResult] = None
    containing_work_zone: Optional[Dict[str, Any]] = None
    nearest_refuge: Optional[RefugeResult] = None
    nearby_trains: List[SpatialTrainResult] = []


class PaginatedSpatialResult(BaseModel):
    total_count: int
    limit: int
    offset: int
    items: List[Any]
