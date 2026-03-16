import pytest
from datetime import datetime, timezone

def test_metrics_lifecycle(client):
    # 1. Create a record
    metric_data = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "height_cm": 175.5,
        "weight_kg": 72.3,
        "bust_cm": 95.0,
        "waist_cm": 80.0,
        "hips_cm": 98.0
    }
    resp = client.post("/api/v1/metrics/", json=metric_data)
    assert resp.status_code == 200
    created_data = resp.json()
    assert created_data["height_cm"] == 175.5
    metric_id = created_data["id"]

    # 2. List records
    resp = client.get("/api/v1/metrics/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1

    # 3. Get latest
    resp = client.get("/api/v1/metrics/latest")
    assert resp.status_code == 200
    assert resp.json()["id"] == metric_id

    # 4. Delete record
    resp = client.delete(f"/api/v1/metrics/{metric_id}")
    assert resp.status_code == 200
    
    # 5. Verify deletion
    resp = client.get(f"/api/v1/metrics/latest")
    # If it was the only record, latest might return 404 or a different record
    # For a clean test enviroment, we check if the ID is gone or 404
    if resp.status_code == 200:
        assert resp.json()["id"] != metric_id
