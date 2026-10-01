import pytest
from datetime import datetime, timezone
from app.services.integration_service import IntegrationAdapterService
from app.schemas.integration import TrainPositionIngest, BlockStatusIngest, WorkOrderIngest, EmergencyIngest

def test_train_position_ingest_accepted(db_session):
    adapter = IntegrationAdapterService(db_session)
    payload = TrainPositionIngest(
        train_id="TRN-EXT-999",
        number="12626",
        name="Test Express",
        line="DOWN",
        block_section_code="MAS-AJJ-DOWN-120",
        latitude=13.0827,
        longitude=80.2707,
        speed_kmh=95.0,
        heading_degrees=90.0,
        direction="EASTBOUND",
        source_system_id="TEST-INTEGRATION-PROVIDER",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    result = adapter.process_train_position_ingest(payload, "corr-test-999")
    assert result.status == "ACCEPTED"
    assert result.entity_id == "TRN-EXT-999"
    assert len(result.warnings) == 0

def test_stale_telemetry_degraded_status(db_session):
    adapter = IntegrationAdapterService(db_session)
    stale_timestamp = "2020-01-01T00:00:00Z"
    payload = TrainPositionIngest(
        train_id="TRN-EXT-888",
        number="12627",
        name="Stale Express",
        line="UP",
        block_section_code="MAS-AJJ-DOWN-120",
        latitude=13.0827,
        longitude=80.2707,
        speed_kmh=80.0,
        heading_degrees=90.0,
        direction="WESTBOUND",
        source_system_id="TEST-STALE-PROVIDER",
        timestamp=stale_timestamp,
    )
    result = adapter.process_train_position_ingest(payload, "corr-test-888")
    assert result.status == "DEGRADED"
    assert any("Stale telemetry" in w for w in result.warnings)

def test_block_status_ingest(db_session):
    adapter = IntegrationAdapterService(db_session)
    payload = BlockStatusIngest(
        block_section_code="MAS-AJJ-DOWN-120",
        status="MAINTENANCE",
        line_type="DOWN",
        speed_limit_kmh=60,
        source_system_id="AXLE-COUNTER-MAS",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    result = adapter.process_block_status_ingest(payload, "corr-test-block")
    assert result.status == "ACCEPTED"
    assert result.normalized_data["status"] == "MAINTENANCE"

def test_work_order_ingest(db_session):
    adapter = IntegrationAdapterService(db_session)
    payload = WorkOrderIngest(
        work_zone_id="WZ-EXT-777",
        name="Night Section Work",
        block_section_code="MAS-AJJ-DOWN-120",
        assigned_team_code="GANG-04",
        buffer_zone_meters=500.0,
        safety_zone_meters=200.0,
        source_system_id="TMS-WORK-ORDERS",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    result = adapter.process_work_order_ingest(payload, "corr-test-wz")
    assert result.status == "ACCEPTED"
    assert result.entity_id == "WZ-EXT-777"

def test_simulated_external_provider_tick(db_session):
    adapter = IntegrationAdapterService(db_session)
    res = adapter.run_simulated_external_provider_tick()
    assert res["simulation_tick"] == "COMPLETED"
    assert res["provider"] == "SIMULATED-RAILWAY-CONTROL-CENTER"
    assert res["result"]["status"] == "ACCEPTED"

def test_integration_contracts_api(client):
    response = client.get("/api/v1/integration/contracts")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "WGS84 / EPSG:4326" in data["coordinate_system"]
    assert "AUTHORIZED-INTEGRATION-READY" in data["safety_policy"]
