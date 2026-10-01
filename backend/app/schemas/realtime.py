from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class EventEnvelope(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str  # TRAIN_POSITION_UPDATE, WORKER_LOCATION_UPDATE, ALERT_CREATED, ALERT_ACKNOWLEDGED, EMERGENCY_TRIGGERED, etc.
    schema_version: int = 1
    occurred_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    source: str = "BACKEND"  # SIMULATOR, BACKEND, WORKER_DEVICE
    correlation_id: Optional[str] = None
    entity_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)


class WebSocketMessage(BaseModel):
    type: str  # SUBSCRIBE, UNSUBSCRIBE, PING, ACK, EVENT, SNAPSHOT, HEARTBEAT, ERROR, SUBSCRIPTION_ACK
    sequence: Optional[int] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    payload: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class SnapshotData(BaseModel):
    snapshot_version: int = 1
    last_event_sequence: int = 0
    workers: List[Dict[str, Any]]
    trains: List[Dict[str, Any]]
    work_zones: List[Dict[str, Any]]
    alerts: List[Dict[str, Any]]
    near_misses: List[Dict[str, Any]]
    system_health: Dict[str, Any]
