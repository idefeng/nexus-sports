from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BodyMetricsBase(BaseModel):
    recorded_at: Optional[datetime] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bust_cm: Optional[float] = None
    waist_cm: Optional[float] = None
    hips_cm: Optional[float] = None

class BodyMetricsCreate(BodyMetricsBase):
    pass

class BodyMetricsUpdate(BodyMetricsBase):
    pass

class BodyMetricsRead(BodyMetricsBase):
    id: int
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
