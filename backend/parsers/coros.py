import os
from typing import List
from datetime import datetime, timezone
import fitparse
import gpxpy
import polyline

from backend.parsers.base import BaseParser
from backend.schemas.activity import ActivityCreate

class CorosParser(BaseParser):
    def parse(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.fit':
            return self._parse_fit(file_path, original_file_hash)
        elif ext == '.gpx':
            return self._parse_gpx(file_path, original_file_hash)
        else:
            raise ValueError(f"Unsupported file extension {ext} for Coros parser")

    def _parse_fit(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        fitfile = fitparse.FitFile(file_path)
        activities = []
        
        # Simple extraction logic for MVP
        activity_type = "Unknown"
        start_time = None
        end_time = None
        duration_s = 0.0
        distance_m = 0.0
        
        # Process messages
        points = []
        for record in fitfile.get_messages('session'):
            for data in record:
                if data.name == 'sport':
                    activity_type = str(data.value).title()
                elif data.name == 'start_time':
                    start_time = data.value
                elif data.name == 'total_elapsed_time':
                    duration_s = float(data.value)
                elif data.name == 'total_distance':
                    distance_m = float(data.value)
                    
        # Extract track points
        for record in fitfile.get_messages('record'):
            lat, lon = None, None
            for data in record:
                if data.name == 'position_lat' and data.value:
                    lat = data.value * (180.0 / 2**31) # convert semicircles to degrees
                elif data.name == 'position_long' and data.value:
                    lon = data.value * (180.0 / 2**31)
            
            if lat is not None and lon is not None:
                points.append((lat, lon))
        
        poly = polyline.encode(points) if points else None
        
        if not start_time:
            start_time = datetime.now()
        if not end_time:
            import datetime as dt
            end_time = start_time + dt.timedelta(seconds=duration_s)
            
        activity = ActivityCreate(
            activity_type=activity_type,
            start_time=start_time,
            end_time=end_time,
            duration_s=duration_s,
            distance_m=distance_m,
            source_device="Coros",
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
                
                # Length 2d is in meters
                distance_m = track.length_2d()
                
                # Create polyline
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
                    source_device="Coros",
                    original_file_hash=original_file_hash,
                    polyline=poly
                )
                activities.append(activity)
                
        return activities
