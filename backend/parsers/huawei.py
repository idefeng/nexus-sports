import json
import os
import zipfile
import tempfile
import polyline
from datetime import datetime
from typing import List, Optional
from backend.parsers.base import BaseParser
from backend.schemas.activity import ActivityCreate
from backend.core.config import logger


class HuaweiParser(BaseParser):
    """
    Parser for Huawei Health data exported as a ZIP archive.
    
    Structure handled:
    - ZIP file contains 'MotionPathDetail' directory.
    - Inside are JSON files with activity details and 'HiTrack' files.
    """

    def parse(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        activities = []
        
        if not zipfile.is_zipfile(file_path):
            # Fallback if it's a single JSON file (unlikely from Huawei export but good for testing)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    activity = self._parse_single_json(data, original_file_hash)
                    if activity:
                        activities.append(activity)
            except:
                pass
            return activities

        with zipfile.ZipFile(file_path, 'r') as z:
            # Look for MotionPathDetail JSON files
            for info in z.infolist():
                if "MotionPathDetail" in info.filename and info.filename.endswith(".json"):
                    try:
                        with z.open(info.filename) as f:
                            data = json.load(f)
                            # Handle different possible JSON structures (List or Object)
                            if isinstance(data, list):
                                for item in data:
                                    act = self._parse_single_json(item, f"{original_file_hash}_{info.CRC}")
                                    if act: activities.append(act)
                            else:
                                act = self._parse_single_json(data, f"{original_file_hash}_{info.CRC}")
                                if act: activities.append(act)
                    except Exception as e:
                        logger.error("Error parsing %s in %s: %s", info.filename, file_path, e)
                        
        return activities

    def _parse_single_json(self, data: dict, file_hash: str) -> Optional[ActivityCreate]:
        """
        Parses a single Huawei MotionPathDetail JSON object.
        """
        try:
            # Basic stats
            # Huawei fields can vary. Common ones:
            # sportType: 1=Run, 2=Cycle, etc.
            sport_type_code = data.get("sportType", 0)
            sport_map = {1: "Running", 2: "Cycling", 3: "Walking", 9: "Swimming", 0: "Other"}
            activity_type = sport_map.get(sport_type_code, "Other")
            
            # Times are usually ms timestamps
            start_ms = data.get("startTime")
            end_ms = data.get("endTime")
            if not start_ms or not end_ms:
                return None
                
            start_time = datetime.fromtimestamp(start_ms / 1000)
            end_time = datetime.fromtimestamp(end_ms / 1000)
            duration_s = (end_ms - start_ms) / 1000
            
            # Metrics
            distance_m = data.get("totalDistance", 0.0)
            calories_kcal = data.get("totalCalories", 0.0) / 1000.0 # Huawei often stores as cal or kcal depending on version
            
            # Points for Polyline
            point_list = data.get("pointList", [])
            coords = []
            for pt in point_list:
                # pt is usually "lat;lon;alt;time;hr;..."
                if isinstance(pt, str):
                    parts = pt.split(";")
                    if len(parts) >= 2:
                        coords.append((float(parts[0]), float(parts[1])))
                elif isinstance(pt, dict):
                    lat = pt.get("latitude") or pt.get("lat")
                    lon = pt.get("longitude") or pt.get("lon")
                    if lat and lon:
                        coords.append((float(lat), float(lon)))
            
            res_polyline = polyline.encode(coords) if coords else None
            
            # Avg metrics
            avg_hr = data.get("avgHeartRate")
            avg_pace = data.get("avgPace") # s/km
            
            return ActivityCreate(
                activity_type=activity_type,
                start_time=start_time,
                end_time=end_time,
                duration_s=duration_s,
                distance_m=distance_m,
                avg_pace_s_per_km=avg_pace,
                avg_heart_rate=avg_hr,
                calories_kcal=calories_kcal,
                source_device="Huawei Health",
                original_file_hash=file_hash,
                polyline=res_polyline
            )
        except Exception as e:
            logger.error("Huawei parsing item error: %s", e)
            return None
