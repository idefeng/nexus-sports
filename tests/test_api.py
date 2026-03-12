"""
Tests for the API endpoints.
"""
import os
import pytest


class TestHealthEndpoint:
    def test_health_check(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"


class TestActivitiesEndpoint:
    def test_get_activities_empty(self, client):
        resp = client.get("/api/v1/activities")
        assert resp.status_code == 200
        data = resp.json()
        assert "total" in data
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_get_activities_with_pagination(self, client):
        resp = client.get("/api/v1/activities?skip=0&limit=10")
        assert resp.status_code == 200
        data = resp.json()
        assert data["skip"] == 0
        assert data["limit"] == 10

    def test_get_activity_not_found(self, client):
        resp = client.get("/api/v1/activities/99999")
        assert resp.status_code == 404

    def test_delete_activity_not_found(self, client):
        resp = client.delete("/api/v1/activities/99999")
        assert resp.status_code == 404


class TestStatsEndpoint:
    def test_get_stats_summary_empty(self, client):
        resp = client.get("/api/v1/stats/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert "total_activities" in data

    def test_get_stats_trend(self, client):
        resp = client.get("/api/v1/stats/trend")
        assert resp.status_code == 200
        data = resp.json()
        assert "trends" in data

    def test_get_stats_distribution(self, client):
        resp = client.get("/api/v1/stats/distribution")
        assert resp.status_code == 200
        data = resp.json()
        assert "distribution" in data


class TestAgentEndpoint:
    def test_get_latest_activity_empty(self, client):
        resp = client.get("/api/v1/agent/latest_activity")
        assert resp.status_code == 200
        data = resp.json()
        assert "report" in data

    def test_get_monthly_report(self, client):
        resp = client.get("/api/v1/agent/monthly_report?target_month=2026-03")
        assert resp.status_code == 200
        data = resp.json()
        assert "report" in data

    def test_get_monthly_report_invalid_format(self, client):
        resp = client.get("/api/v1/agent/monthly_report?target_month=invalid")
        assert resp.status_code == 400


class TestUploadEndpoint:
    def test_upload_unsupported_format(self, client):
        """Uploading a .txt file should be rejected."""
        resp = client.post(
            "/api/v1/upload",
            files=[("files", ("test.txt", b"hello world", "text/plain"))]
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["results"][0]["status"] == "error"

    def test_upload_empty_file(self, client):
        """Uploading an empty .fit file should be rejected."""
        resp = client.post(
            "/api/v1/upload",
            files=[("files", ("empty.fit", b"", "application/octet-stream"))]
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["results"][0]["status"] == "error"

    def test_upload_real_fit_file(self, client, sample_fit_path):
        """Upload a real FIT file and verify it's processed."""
        with open(sample_fit_path, "rb") as f:
            filename = os.path.basename(sample_fit_path)
            resp = client.post(
                "/api/v1/upload",
                files=[("files", (filename, f.read(), "application/octet-stream"))]
            )
        assert resp.status_code == 200
        data = resp.json()
        result = data["results"][0]
        assert result["status"] in ("success", "skipped")


class TestPatchEndpoint:
    def test_patch_activity_not_found(self, client):
        resp = client.patch("/api/v1/activities/99999", json={"activity_type": "Swimming"})
        assert resp.status_code == 404

    def test_patch_activity_type(self, client, sample_fit_path):
        """Upload a file, then PATCH the activity type."""
        # First upload a file to create an activity
        with open(sample_fit_path, "rb") as f:
            filename = os.path.basename(sample_fit_path)
            client.post(
                "/api/v1/upload",
                files=[("files", (filename, f.read(), "application/octet-stream"))]
            )

        # Get activities to find the ID
        resp = client.get("/api/v1/activities?limit=1")
        activities = resp.json()["items"]
        if len(activities) == 0:
            pytest.skip("No activities created from upload")

        activity_id = activities[0]["id"]

        # PATCH the activity type
        resp = client.patch(f"/api/v1/activities/{activity_id}", json={"activity_type": "Swimming"})
        assert resp.status_code == 200
        assert resp.json()["activity_type"] == "Swimming"

        # Verify the change persisted
        resp = client.get(f"/api/v1/activities/{activity_id}")
        assert resp.json()["activity_type"] == "Swimming"


class TestCRUDLifecycle:
    def test_full_crud_lifecycle(self, client, sample_fit_path):
        """Test complete Create → Read → Update → Delete lifecycle."""
        # CREATE: Upload file
        with open(sample_fit_path, "rb") as f:
            filename = os.path.basename(sample_fit_path)
            resp = client.post(
                "/api/v1/upload",
                files=[("files", (filename, f.read(), "application/octet-stream"))]
            )
        assert resp.status_code == 200

        # READ: Get activities
        resp = client.get("/api/v1/activities")
        data = resp.json()
        assert data["total"] > 0
        activity_id = data["items"][0]["id"]

        # READ single
        resp = client.get(f"/api/v1/activities/{activity_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == activity_id

        # UPDATE: PATCH activity
        resp = client.patch(f"/api/v1/activities/{activity_id}", json={"activity_type": "Cycling"})
        assert resp.status_code == 200
        assert resp.json()["activity_type"] == "Cycling"

        # DELETE: Remove activity
        resp = client.delete(f"/api/v1/activities/{activity_id}")
        assert resp.status_code == 200

        # Verify deletion
        resp = client.get(f"/api/v1/activities/{activity_id}")
        assert resp.status_code == 404


class TestExportEndpoint:
    def test_export_original_not_found(self, client):
        resp = client.get("/api/v1/export/original/99999")
        assert resp.status_code == 404

    def test_export_gpx_not_found(self, client):
        resp = client.get("/api/v1/export/gpx/99999")
        assert resp.status_code == 404

