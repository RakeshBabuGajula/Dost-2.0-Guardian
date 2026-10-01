def test_list_workers(client):
    response = client.get("/api/v1/workers")
    assert response.status_code == 200
    workers = response.json()
    assert isinstance(workers, list)
    assert len(workers) >= 1
    worker_ids = [w["id"] for w in workers]
    assert "WRK-101" in worker_ids


def test_get_worker_detail(client):
    response = client.get("/api/v1/workers/WRK-101")
    assert response.status_code == 200
    worker = response.json()
    assert worker["name"] == "Ramesh Kumar"
    assert "envelope" in worker


def test_get_worker_not_found(client):
    response = client.get("/api/v1/workers/WRK-99999")
    assert response.status_code == 404
