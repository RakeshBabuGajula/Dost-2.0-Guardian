def test_list_trains(client):
    response = client.get("/api/v1/trains")
    assert response.status_code == 200
    trains = response.json()
    assert isinstance(trains, list)
    assert len(trains) >= 1
    assert trains[0]["id"] == "TRN-204"
