import uuid


def test_idempotent_emergency_event(client):
    unique_event_id = f"test-evt-{uuid.uuid4()}"
    payload = {
        "event_id": unique_event_id,
        "worker_id": "WRK-101",
        "trigger_type": "MANUAL_SOS",
        "block_section_code": "MAS-AJJ-DOWN-120",
    }

    # First attempt: ACKNOWLEDGED
    res1 = client.post("/api/v1/emergency-events", json=payload)
    assert res1.status_code == 200
    assert res1.json()["status"] == "ACKNOWLEDGED"

    # Second attempt with same event_id: DUPLICATE_IGNORED
    res2 = client.post("/api/v1/emergency-events", json=payload)
    assert res2.status_code == 200
    assert res2.json()["status"] == "DUPLICATE_IGNORED"
