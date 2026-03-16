from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.core.database import Base
from datetime import datetime, timezone

def _utcnow():
    return datetime.now(timezone.utc)

class BodyMetrics(Base):
    __tablename__ = "body_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=True)  # Reserved for multi-tenant
    
    recorded_at = Column(DateTime, index=True, default=_utcnow)
    
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    
    bust_cm = Column(Float, nullable=True)
    waist_cm = Column(Float, nullable=True)
    hips_cm = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
