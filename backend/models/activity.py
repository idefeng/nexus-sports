from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.core.database import Base
from datetime import datetime, timezone


def _utcnow():
    return datetime.now(timezone.utc)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)  # Reserved for multi-tenant
    
    # Basic Info
    activity_type = Column(String, index=True)  # e.g., Run, Bike, Swim
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime)
    duration_s = Column(Float)  # Total duration in seconds
    distance_m = Column(Float)  # Total distance in meters
    
    # Sport Metrics
    avg_pace_s_per_km = Column(Float, nullable=True)
    avg_heart_rate = Column(Float, nullable=True)
    avg_cadence = Column(Float, nullable=True)
    avg_stride_length_m = Column(Float, nullable=True)
    total_ascent_m = Column(Float, nullable=True)
    calories_kcal = Column(Float, nullable=True)
    
    # Physiological Data
    training_load = Column(Float, nullable=True)
    recovery_time_h = Column(Float, nullable=True)
    vo2max = Column(Float, nullable=True)
    
    # Track Data
    polyline = Column(String, nullable=True)  # Compressed GPS polyline
    
    # Metadata
    source_device = Column(String)  # e.g., Huawei, Coros
    original_file_hash = Column(String, unique=True, index=True)  # For idempotency
    
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)


class ImportRecord(Base):
    """Data Lineage and Error Logs"""
    __tablename__ = "import_records"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    file_hash = Column(String, unique=True, index=True)
    status = Column(String)  # 'success', 'failed', 'skipped'
    error_message = Column(String, nullable=True)
    imported_at = Column(DateTime, default=_utcnow)
