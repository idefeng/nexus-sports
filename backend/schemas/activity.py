from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class ActivityBase(BaseModel):
    activity_type: str = Field(..., description="Type of sport")
    start_time: datetime
    end_time: datetime
    duration_s: float
    distance_m: float
    
    avg_pace_s_per_km: Optional[float] = None
    avg_heart_rate: Optional[float] = None
    avg_cadence: Optional[float] = None
    avg_stride_length_m: Optional[float] = None
    total_ascent_m: Optional[float] = None
    calories_kcal: Optional[float] = None
    
    training_load: Optional[float] = None
    recovery_time_h: Optional[float] = None
    vo2max: Optional[float] = None
    
    polyline: Optional[str] = None
    notes: Optional[str] = None
    source_device: str
    original_file_hash: str

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    """Partial update schema — all fields optional."""
    activity_type: Optional[str] = None
    distance_m: Optional[float] = None
    duration_s: Optional[float] = None
    calories_kcal: Optional[float] = None
    avg_heart_rate: Optional[float] = None
    avg_cadence: Optional[float] = None
    total_ascent_m: Optional[float] = None
    notes: Optional[str] = None

class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ImportRecordResponse(BaseModel):
    id: int
    file_name: str
    file_hash: str
    status: str
    error_message: Optional[str]
    imported_at: datetime

    model_config = ConfigDict(from_attributes=True)
