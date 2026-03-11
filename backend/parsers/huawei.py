import zipfile
import json
import os
from tempfile import TemporaryDirectory
from typing import List
from datetime import datetime

from backend.parsers.base import BaseParser
from backend.schemas.activity import ActivityCreate

class HuaweiParser(BaseParser):
    def parse(self, file_path: str, original_file_hash: str) -> List[ActivityCreate]:
        activities = []
        
        # Skeleton for Huawei ZIP processing
        # Real implementation would scan for "Motion path" JSON or similar schemas inside the exported ZIP
        with TemporaryDirectory() as tmpdirname:
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdirname)
                    # For MVP, just return a dummy processed activity.
                    # TODO: Implement actual traversing of Huawei JSON schema.
                    pass
        
        # dummy fallback if nothing found or for MVP demo
        activity = ActivityCreate(
            activity_type="Run",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration_s=1800,
            distance_m=5000,
            source_device="Huawei",
            original_file_hash=original_file_hash,
            polyline=None
        )
        activities.append(activity)
            
        return activities
