import os
from typing import List
from datetime import datetime, timezone
import fitparse
import gpxpy
import polyline

from backend.parsers.base import BaseParser
from backend.schemas.activity import ActivityCreate
from backend.utils.fitparse_patch import apply_patch

# Apply monkey patch to avoid crashing on Coros FIT valid files with invalid field sizes
apply_patch()

class FitGpxParser(BaseParser):
    """
    Generic FIT and GPX parser supporting multiple manufacturers (Coros, Garmin, etc.)
    """
    
    MANUFACTURER_MAP = {
        1: "Garmin",
        15: "Suunto",
        22: "Polar",
        31: "Polar",
        32: "Wahoo",
        38: "The Sufferfest",
        81: "Coros",
        254: "Huawei",
        294: "Coros",
        255: "Development",
        265: "Apple",
        266: "Apple",
    }

    def parse(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.fit':
            return self._parse_fit(file_path, original_file_hash)
        elif ext == '.gpx':
            return self._parse_gpx(file_path, original_file_hash)
        else:
            raise ValueError(f"Unsupported file extension {ext} for FIT/GPX parser")

    def _parse_fit(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        from backend.core.config import logger
        fitfile = fitparse.FitFile(file_path)
        activities = []
        
        # Detect manufacturer
        source_device = "Unknown FIT Device"
        manufacturer_id = None
        product_name = None
        
        for record in fitfile.get_messages('file_id'):
            manufacturer_id = record.get_value('manufacturer')
            product_name = record.get_value('product_name')
            if manufacturer_id in self.MANUFACTURER_MAP:
                source_device = self.MANUFACTURER_MAP[manufacturer_id]
                break
        
        # Backup check in device_info if file_id search failed
        if source_device == "Unknown FIT Device":
            for record in fitfile.get_messages('device_info'):
                manufacturer_id = record.get_value('manufacturer')
                if manufacturer_id in self.MANUFACTURER_MAP:
                    source_device = self.MANUFACTURER_MAP[manufacturer_id]
                    break
        
        # Backup identification via product_name string
        if source_device == "Unknown FIT Device" or source_device == "Development":
            if product_name and "COROS" in str(product_name).upper():
                source_device = str(product_name)
            elif product_name:
                source_device = str(product_name)

        logger.info("FIT Device detection: manufacturer=%s, product=%s -> %s", 
                    manufacturer_id, product_name, source_device)
        
        # Core fields
        activity_type = "Unknown"
        start_time = None
        duration_s = 0.0
        distance_m = 0.0
        
        # Sport metrics
        avg_heart_rate = None
        avg_cadence = None
        avg_stride_length_m = None
        total_ascent_m = None
        calories_kcal = None
        avg_pace_s_per_km = None
        training_load = None
        vo2max = None
        avg_speed = None
        
        # Process session messages
        for record in fitfile.get_messages('session'):
            for data in record:
                if data.name == 'sport' and data.value:
                    activity_type = str(data.value).title()
                elif data.name == 'start_time' and data.value:
                    start_time = data.value
                elif data.name == 'total_elapsed_time' and data.value:
                    duration_s = float(data.value)
                elif data.name == 'total_distance' and data.value:
                    distance_m = float(data.value)
                elif data.name == 'avg_heart_rate' and data.value:
                    avg_heart_rate = float(data.value)
                elif data.name in ('avg_cadence', 'avg_running_cadence') and data.value:
                    avg_cadence = float(data.value)
                elif data.name == 'avg_stride_length' and data.value:
                    val = float(data.value)
                    avg_stride_length_m = val / 100.0 if val > 10 else val
                elif data.name == 'total_ascent' and data.value:
                    total_ascent_m = float(data.value)
                elif data.name == 'total_calories' and data.value:
                    calories_kcal = float(data.value)
                elif data.name in ('enhanced_avg_speed', 'avg_speed') and data.value:
                    avg_speed = float(data.value)
                elif data.name == 'total_training_effect' and data.value:
                    training_load = float(data.value)
                elif data.name == 'training_stress_score' and data.value:
                    if training_load is None:
                        training_load = float(data.value)
                elif data.name == 'vo2_max' and data.value:
                    vo2max = float(data.value)
        
        if avg_speed and avg_speed > 0:
            avg_pace_s_per_km = 1000.0 / avg_speed
                    
        points = []
        for record in fitfile.get_messages('record'):
            lat, lon = None, None
            for data in record:
                if data.name == 'position_lat' and data.value:
                    lat = data.value * (180.0 / 2**31)
                elif data.name == 'position_long' and data.value:
                    lon = data.value * (180.0 / 2**31)
            if lat is not None and lon is not None:
                points.append((lat, lon))
        
        poly = polyline.encode(points) if points else None
        
        if not start_time:
            start_time = datetime.now()
        
        from datetime import timedelta
        end_time = start_time + timedelta(seconds=duration_s)
            
        activity = ActivityCreate(
            activity_type=activity_type,
            start_time=start_time,
            end_time=end_time,
            duration_s=duration_s,
            distance_m=distance_m,
            avg_pace_s_per_km=avg_pace_s_per_km,
            avg_heart_rate=avg_heart_rate,
            avg_cadence=avg_cadence,
            avg_stride_length_m=avg_stride_length_m,
            total_ascent_m=total_ascent_m,
            calories_kcal=calories_kcal,
            training_load=training_load,
            vo2max=vo2max,
            source_device=source_device,
            original_file_hash=original_file_hash,
            polyline=poly
        )
        activities.append(activity)
        return activities

    def _parse_gpx(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        activities = []
        with open(file_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            
            for track in gpx.tracks:
                start_time = track.get_time_bounds().start_time or datetime.now()
                end_time = track.get_time_bounds().end_time or datetime.now()
                duration_s = track.get_duration() or 0.0
                distance_m = track.length_2d()
                
                points = []
                for segment in track.segments:
                    for point in segment.points:
                        points.append((point.latitude, point.longitude))
                poly = polyline.encode(points) if points else None
                
                activity = ActivityCreate(
                    activity_type=track.type or "Unknown",
                    start_time=start_time,
                    end_time=end_time,
                    duration_s=duration_s,
                    distance_m=distance_m,
                    source_device="GPX Export",
                    original_file_hash=original_file_hash,
                    polyline=poly
                )
                activities.append(activity)
        return activities
