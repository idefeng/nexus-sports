"""
Tests for the Coros FIT/GPX parser.
"""
import os
import pytest
from backend.parsers.fit_gpx import FitGpxParser
from backend.utils.hash import calculate_file_hash


class TestCorosFitParser:
    """Test FIT file parsing with real data files."""

    def test_parse_fit_returns_activities(self, sample_fit_path):
        parser = FitGpxParser()
        file_hash = calculate_file_hash(sample_fit_path)
        activities = parser.parse(sample_fit_path, file_hash)
        
        assert len(activities) >= 1
        act = activities[0]
        # Should be 'Coros' or 'Unknown FIT Device' depending on file content
        assert "FIT" in act.source_device or act.source_device == "Coros"
        assert act.original_file_hash == file_hash

    def test_parse_fit_basic_fields(self, sample_fit_path):
        parser = FitGpxParser()
        activities = parser.parse(sample_fit_path, "test_hash")
        act = activities[0]
        
        assert act.activity_type != "Unknown"
        assert act.start_time is not None
        assert act.end_time is not None
        assert act.duration_s > 0

    def test_parse_fit_extracts_sport_metrics(self, sample_fit_path):
        """Verify that the enhanced parser extracts at least some sport metrics."""
        parser = FitGpxParser()
        activities = parser.parse(sample_fit_path, "test_hash")
        act = activities[0]
        
        # At least some of these should be populated for a real FIT file
        has_metrics = any([
            act.calories_kcal is not None,
            act.avg_heart_rate is not None,
            act.total_ascent_m is not None,
        ])
        assert has_metrics, "Expected at least one sport metric to be extracted from a real FIT file"

    def test_parse_fit_polyline_for_outdoor(self):
        """Outdoor activities should have GPS polyline data."""
        test_files = [
            "data/龙岩市_登山20230408120415.fit",
            "data/跑步20260311233629.fit",
        ]
        parser = FitGpxParser()
        for path in test_files:
            if os.path.exists(path):
                activities = parser.parse(path, "test_hash")
                act = activities[0]
                assert act.polyline is not None, f"Expected polyline for outdoor file {path}"
                return
        pytest.skip("No outdoor FIT file available")

    def test_parse_unsupported_extension_raises(self):
        parser = FitGpxParser()
        with pytest.raises(ValueError, match="Unsupported file extension"):
            parser.parse("fake.txt", "hash")


class TestCorosGpxParser:
    """Test GPX file parsing with real data files."""

    def test_parse_gpx_returns_activities(self, sample_gpx_path):
        parser = FitGpxParser()
        file_hash = calculate_file_hash(sample_gpx_path)
        activities = parser.parse(sample_gpx_path, file_hash)
        
        assert len(activities) >= 1
        act = activities[0]
        assert act.source_device == "GPX Export"
        assert act.polyline is not None  # GPX should always have coordinates
        assert act.distance_m > 0

        assert act.start_time is not None
        assert act.end_time is not None
        assert act.duration_s >= 0


class TestHuaweiParser:
    """Test Huawei Health ZIP parsing with mock data."""

    def test_parse_huawei_zip(self, tmp_path):
        import zipfile
        import json
        from backend.parsers.huawei import HuaweiParser

        # Create a mock Huawei ZIP
        zip_path = tmp_path / "huawei_export.zip"
        motion_path_json = {
            "sportType": 1,  # Running
            "startTime": 1672531200000,  # 2023-01-01 00:00:00
            "endTime": 1672534800000,    # 2023-01-01 01:00:00
            "totalDistance": 10000,
            "totalCalories": 600000,
            "avgHeartRate": 150,
            "avgPace": 360,
            "pointList": [
                "39.9042;116.4074;50;1672531200000;140",
                "39.9142;116.4174;55;1672531500000;145"
            ]
        }
        
        with zipfile.ZipFile(zip_path, "w") as z:
            z.writestr("MotionPathDetail/MotionPathDetail_1.json", json.dumps(motion_path_json))

        parser = HuaweiParser()
        activities = parser.parse(str(zip_path), "huawei_test_hash")
        
        assert len(activities) == 1
        act = activities[0]
        assert act.activity_type == "Running"
        assert act.distance_m == 10000
        assert act.avg_heart_rate == 150
        assert act.source_device == "Huawei Health"
        assert act.polyline is not None

