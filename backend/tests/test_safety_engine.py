import pytest
from app.db.session import SessionLocal
from app.services.safety_engine import SafetyEngine, OperationalSafetyConfig
from app.services.alert_service import create_or_update_alert, acknowledge_alert, escalate_alert
from app.services.emergency_service import trigger_emergency_sos, resolve_emergency
from app.services.near_miss_service import record_near_miss
from app.models.domain_models import Alert, Worker, NearMiss, EmergencyEvent


def test_dynamic_safety_envelope_expansion_on_gps_loss():
    # Normal GPS accuracy (2.5m)
    env_normal = SafetyEngine.calculate_dynamic_envelope(gps_accuracy_meters=2.5)
    assert env_normal["isExpandedDueToGps"] is False
    assert env_normal["radiusMeters"] == 552.5

    # Degraded GPS accuracy (42.0m)
    env_degraded = SafetyEngine.calculate_dynamic_envelope(gps_accuracy_meters=42.0)
    assert env_degraded["isExpandedDueToGps"] is True
    assert env_degraded["radiusMeters"] > 700.0


def test_time_to_danger_calculation():
    # 110 km/h = 30.55 m/s. 1100m distance -> 36 seconds
    ttd, formatted = SafetyEngine.calculate_time_to_danger(distance_meters=1100.0, train_speed_kmh=110.0)
    assert ttd == 36
    assert formatted == "00:36"

    # 0 speed case
    ttd_zero, formatted_zero = SafetyEngine.calculate_time_to_danger(distance_meters=500.0, train_speed_kmh=0.0)
    assert ttd_zero == 0
    assert formatted_zero == "00:00"


def test_evaluate_worker_train_safety_safe_state():
    eval_result = SafetyEngine.evaluate_worker_train_safety(
        worker_id="WRK-101",
        worker_x=450.0,
        worker_y=140.0,
        worker_gps_accuracy=2.5,
        train_id="TRN-204",
        train_number="12626",
        train_name="MAS-SBC Express",
        train_x=500.0,  # Train has already passed worker X=450
        train_speed_kmh=110.0,
        train_direction="EASTBOUND",
        block_section_code="MAS-AJJ-DOWN-120",
    )
    assert eval_result["state"] == "SAFE"


def test_evaluate_worker_train_safety_critical_state():
    eval_result = SafetyEngine.evaluate_worker_train_safety(
        worker_id="WRK-101",
        worker_x=450.0,
        worker_y=140.0,
        worker_gps_accuracy=2.5,
        train_id="TRN-204",
        train_number="12626",
        train_name="MAS-SBC Express",
        train_x=250.0,  # Train approaching X=450 (distance 200m -> TTD ~6s)
        train_speed_kmh=110.0,
        train_direction="EASTBOUND",
        block_section_code="MAS-AJJ-DOWN-120",
    )
    assert eval_result["state"] in ["CRITICAL", "EMERGENCY"]
    assert eval_result["escalation_tier"] in ["TIER_1_SUPERVISOR", "TIER_3_CONTROL_ROOM"]


def test_alert_idempotency_and_acknowledgement():
    db = SessionLocal()
    try:
        # Create alert 1
        alert_dict1, is_new1 = create_or_update_alert(
            db=db,
            worker_id="WRK-101",
            worker_name="Ramesh Kumar",
            train_id="TRN-204",
            train_name="MAS-SBC Express",
            block_section_code="MAS-AJJ-DOWN-120",
            state="CRITICAL",
            time_to_danger_seconds=45,
            distance_to_train_meters=1100.0,
        )
        assert alert_dict1["id"] is not None

        # Repeat update for same worker (should update, not create duplicate)
        alert_dict2, is_new2 = create_or_update_alert(
            db=db,
            worker_id="WRK-101",
            worker_name="Ramesh Kumar",
            train_id="TRN-204",
            train_name="MAS-SBC Express",
            block_section_code="MAS-AJJ-DOWN-120",
            state="CRITICAL",
            time_to_danger_seconds=30,
            distance_to_train_meters=800.0,
        )
        assert is_new2 is False
        assert alert_dict2["id"] == alert_dict1["id"]

        # Acknowledge alert
        ack = acknowledge_alert(db, alert_id=alert_dict1["id"], worker_id="WRK-101", acknowledged_by="Ramesh Kumar")
        assert ack["isAcknowledged"] is True
        assert ack["state"] == "SAFE"
    finally:
        db.close()


def test_trigger_emergency_sos():
    db = SessionLocal()
    try:
        ev = trigger_emergency_sos(db, worker_id="WRK-101", trigger_type="MANUAL_SOS")
        assert ev["status"] == "ACTIVE"
        assert ev["workerId"] == "WRK-101"

        resolved = resolve_emergency(db, event_id=ev["eventId"], resolved_by="Control Room")
        assert resolved["status"] == "RESOLVED"
    finally:
        db.close()


def test_record_near_miss():
    db = SessionLocal()
    try:
        nm = record_near_miss(
            db=db,
            worker_id="WRK-101",
            worker_name="Ramesh Kumar",
            train_id="TRN-204",
            train_speed_kmh=110.0,
            block_section_code="MAS-AJJ-DOWN-120",
            min_clearance_meters=1.8,
            ttd_seconds=12,
            severity="MODERATE",
        )
        assert nm["id"].startswith("NM-")
        assert nm["minSpatialClearanceMeters"] == 1.8
    finally:
        db.close()
