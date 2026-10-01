import pytest
from app.services.analytics_service import AnalyticsService
from app.services.ai_service import AIService

def test_analytics_service_kpis(db_session):
    service = AnalyticsService(db_session)
    kpis = service.get_operational_kpis()
    assert "active_workers" in kpis
    assert "active_trains" in kpis
    assert "active_work_zones" in kpis
    assert "alerts" in kpis
    assert kpis["system_status"] == "OPERATIONAL"

def test_analytics_service_timeline(db_session):
    service = AnalyticsService(db_session)
    timeline = service.get_event_timeline(limit=10)
    assert isinstance(timeline, list)

def test_analytics_service_safety_metrics(db_session):
    service = AnalyticsService(db_session)
    metrics = service.get_safety_metrics(timeframe="today")
    assert metrics["timeframe"] == "today"
    assert "total_alerts" in metrics["metrics"]
    assert "severity_distribution" in metrics

def test_analytics_service_heatmap(db_session):
    service = AnalyticsService(db_session)
    heatmap = service.get_safety_heatmap()
    assert isinstance(heatmap, list)

def test_ai_service_query(db_session):
    ai = AIService(db_session)
    res = ai.process_operational_query("SUPERVISOR", "How many critical alerts occurred today?")
    assert res["status"] == "SUCCESS"
    assert res["answer_type"] == "AI-GENERATED ANALYSIS"
    assert "alerts" in res["answer"].lower() or "unacknowledged" in res["answer"].lower()
    assert "AI IS AN ANALYTICAL ASSISTANT ONLY" in res["disclaimer"]

def test_ai_service_query_unauthorized(db_session):
    ai = AIService(db_session)
    res = ai.process_operational_query("UNAUTHORIZED_ROLE", "Show secret data")
    assert res["status"] == "UNAUTHORIZED"

def test_ai_service_report_generation(db_session):
    ai = AIService(db_session)
    report = ai.generate_operational_report("SUPERVISOR", "DAILY_SAFETY_SUMMARY", "today")
    assert report["report_type"] == "DAILY_SAFETY_SUMMARY"
    assert "# DOST GUARDIAN 2.0" in report["markdown_content"]
    assert "FACTUAL OPERATIONAL METRICS" in report["markdown_content"]

def test_ai_service_knowledge_base(db_session):
    ai = AIService(db_session)
    docs = ai.search_knowledge_base("clearance track work")
    assert len(docs) > 0
    assert "Indian Railways Track Work Safety Protocol" in docs[0]["title"]
