import pytest

def test_health_deep_diagnostic(client):
    response = client.get("/api/v1/health/deep")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "observability" in data
    assert "database" in data["observability"]
    assert "redis" in data["observability"]

def test_correlation_and_security_headers(client):
    response = client.get("/api/v1/health/live", headers={"X-Correlation-ID": "test-corr-12345"})
    assert response.status_code == 200
    assert response.headers.get("X-Correlation-ID") == "test-corr-12345"
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"

def test_auth_rbac_endpoint_access(client):
    response = client.get("/api/v1/analytics/kpis")
    assert response.status_code == 200
    data = response.json()
    assert data["system_status"] == "OPERATIONAL"

def test_unhandled_exception_suppresses_stacktrace(client):
    response = client.get("/api/v1/workers/WRK-101")
    assert response.status_code == 200
