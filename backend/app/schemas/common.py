from typing import Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[Any] = None


class HealthStatus(BaseModel):
    status: str = "HEALTHY"
    app_alive: bool = True
    db_connected: bool = True
    redis_connected: bool = True
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
