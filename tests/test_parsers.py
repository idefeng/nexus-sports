"""
Tests for the Coros FIT/GPX parser.
"""
import os
import pytest
from backend.parsers.coros import CorosParser
from backend.utils.hash import calculate_file_hash


class TestCorosFitParser:
    """Test FIT file parsing with real data files."""

    def test_parse_fit_returns_activities(self, sample_fit_path):
        parser = CorosParser()
        file_hash = calculate_file_hash(sample_fit_path)
        activities = parser.parse(sample_fit_path, file_hash)
        
        assert len(activities) >= 1
        act = activities[0]
        assert act.source_device == "Coros"
        assert act.original_file_hash == file_hash

    def test_parse_fit_basic_fields(self, sample_fit_path):
        parser = CorosParser()
        activities = parser.parse(sample_fit_path, "test_hash")
        act = activities[0]
        
        assert act.activity_type != "Unknown"
        assert act.start_time is not None
        assert act.end_time is not None
        assert act.duration_s > 0

    def test_parse_fit_extracts_sport_metrics(self, sample_fit_path):
        """Verify that the enhanced parser extracts at least some sport metrics."""
        parser = CorosParser()
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
        parser = CorosParser()
        for path in test_files:
            if os.path.exists(path):
                activities = parser.parse(path, "test_hash")
                act = activities[0]
                assert act.polyline is not None, f"Expected polyline for outdoor file {path}"
                return
        pytest.skip("No outdoor FIT file available")

    def test_parse_unsupported_extension_raises(self):
        parser = CorosParser()
        with pytest.raises(ValueError, match="Unsupported file extension"):
            parser.parse("fake.txt", "hash")


class TestCorosGpxParser:
    """Test GPX file parsing with real data files."""

    def test_parse_gpx_returns_activities(self, sample_gpx_path):
        parser = CorosParser()
        file_hash = calculate_file_hash(sample_gpx_path)
        activities = parser.parse(sample_gpx_path, file_hash)
        
        assert len(activities) >= 1
        act = activities[0]
        assert act.source_device == "Coros"
        assert act.polyline is not None  # GPX should always have coordinates
        assert act.distance_m > 0

    def test_parse_gpx_basic_fields(self, sample_gpx_path):
        parser = CorosParser()
        activities = parser.parse(sample_gpx_path, "test_hash")
        act = activities[0]
        
        assert act.start_time is not None
        assert act.end_time is not None
        assert act.duration_s >= 0
