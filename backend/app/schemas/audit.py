from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict


class AuditLogBase(BaseModel):
    id: str
    event_id: str
    actor: str
    action: str
    target: str
    timestamp: str
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class AuditLogResponse(AuditLogBase):
    model_config = ConfigDict(from_attributes=True)
