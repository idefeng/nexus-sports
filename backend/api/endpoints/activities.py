from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.core.database import get_db
from backend.models.activity import Activity
from backend.schemas.activity import ActivityResponse

router = APIRouter()

@router.get("/", response_model=List[ActivityResponse])
def get_activities(db: Session = Depends(get_db)):
    # For MVP, just return the list of all activities
    activities = db.query(Activity).order_by(Activity.start_time.desc()).all()
    return activities
