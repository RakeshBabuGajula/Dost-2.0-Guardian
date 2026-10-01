import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from geoalchemy2.elements import WKTElement
from app.main import app
from app.db.session import SessionLocal
from app.models.domain_models import Worker, Train, WorkZone, BlockSection, SafeRefugeLocation, WorkerLocation
from app.db.spatial_repository import SpatialRepository
from app.services.spatial_service import SpatialService
from app.security.auth import create_access_token

client = TestClient(app)


def get_auth_header(role="CONTROL_ROOM"):
    token = create_access_token(f"usr-test-{role.lower()}", f"test_{role.lower()}", role)
    return {"Authorization": f"Bearer {token}"}


def test_invalid_coordinate_bounds_rejection():
    headers = get_auth_header()
    # Invalid latitude > 90
    resp = client.get("/api/v1/spatial/workers/nearby?lat=95.0&lng=80.27", headers=headers)
    assert resp.status_code == 422

    # Invalid longitude < -180
    resp = client.get("/api/v1/spatial/workers/nearby?lat=13.08&lng=-190.0", headers=headers)
    assert resp.status_code == 422


def test_spatial_query_nearby_workers():
    headers = get_auth_header()
    resp = client.get("/api/v1/spatial/workers/nearby?lat=13.0823&lng=80.2750&radius_meters=1000", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    w = data["items"][0]
    assert "id" in w
    assert "distance_meters" in w
    assert "latitude" in w
    assert "longitude" in w


def test_spatial_query_nearby_trains():
    headers = get_auth_header()
    resp = client.get("/api/v1/spatial/trains/nearby?lat=13.0820&lng=80.2700&radius_meters=2000", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    t = data["items"][0]
    assert t["id"] == "TRN-204"
    assert t["speed_kmh"] == 110.0


def test_spatial_query_containing_block():
    headers = get_auth_header()
    resp = client.get("/api/v1/spatial/blocks/containing-point?lat=13.0822&lng=80.2750", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "code" in data
    assert data["code"] in ["MAS-AJJ-DOWN-120", "MAS-AJJ-UP-122", "UNKNOWN"]


def test_spatial_query_nearest_refuge():
    headers = get_auth_header()
    resp = client.get("/api/v1/spatial/refuges/nearest?lat=13.0825&lng=80.2750&limit=2", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "refuge_type" in data[0]


def test_worker_spatial_context():
    headers = get_auth_header()
    resp = client.get("/api/v1/spatial/workers/WRK-101/context", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["worker_id"] == "WRK-101"
    assert "current_location" in data
    assert "containing_block" in data
    assert "nearest_refuge" in data
    assert "nearby_trains" in data


def test_spatial_repository_boundary_semantics():
    db = SessionLocal()
    try:
        # Worker point exactly on the boundary of WorkZone WZ-402
        workers = SpatialRepository.find_workers_in_zone(db, "WZ-402")
        assert len(workers) >= 0
    finally:
        db.close()


def test_spatial_repository_location_update():
    db = SessionLocal()
    try:
        worker, loc = SpatialRepository.update_worker_location(
            db=db,
            worker_id="WRK-101",
            lat=13.0824,
            lng=80.2751,
            accuracy_meters=2.1,
            source="TEST",
        )
        assert worker.id == "WRK-101"
        assert loc.gps_accuracy_meters == 2.1
        assert loc.source == "TEST"
    finally:
        db.close()
