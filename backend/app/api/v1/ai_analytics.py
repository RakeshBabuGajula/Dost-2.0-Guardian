from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.ai_service import AIService
from app.security.auth import get_current_active_user
from app.models.domain_models import User

router = APIRouter(prefix="/ai", tags=["ai_analytics"])

class AIQueryRequest(BaseModel):
    query: str = Field(..., example="How many critical alerts occurred today?")

class AIReportRequest(BaseModel):
    report_type: str = Field(..., example="DAILY_SAFETY_SUMMARY")  # DAILY_SAFETY_SUMMARY, SHIFT_SUMMARY, WORK_ZONE_SUMMARY, NEAR_MISS_SUMMARY, ALERT_SUMMARY
    time_range: str = Field("today", example="today")

class AIKnowledgeQueryRequest(BaseModel):
    query: str = Field(..., example="What is the clearance requirement for track work?")

@router.post("/query")
def process_ai_query(
    request: AIQueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Process natural language operational safety queries.
    Grounded in recorded system data. AI DOES NOT make or override real-time safety decisions.
    """
    ai_service = AIService(db)
    return ai_service.process_operational_query(
        user_role=current_user.role,
        query_text=request.query
    )

@router.post("/reports")
def generate_ai_report(
    request: AIReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """Generate structured markdown operational safety reports."""
    ai_service = AIService(db)
    return ai_service.generate_operational_report(
        user_role=current_user.role,
        report_type=request.report_type,
        time_range=request.time_range
    )

@router.post("/knowledge")
def search_knowledge_base(
    request: AIKnowledgeQueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[Dict[str, Any]]:
    """Search railway standard operating procedures and documentation."""
    ai_service = AIService(db)
    return ai_service.search_knowledge_base(query_text=request.query)
