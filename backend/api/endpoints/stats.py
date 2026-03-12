from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any

from backend.core.database import get_db
from backend.models.activity import Activity

router = APIRouter()

@router.get("/summary", response_model=Dict[str, Any])
def get_stats_summary(db: Session = Depends(get_db)):
    """Get overall statistics summary."""
    total_activities = db.query(Activity).count()
    if total_activities == 0:
        return {
            "total_activities": 0,
            "total_distance_km": 0.0,
            "total_duration_hours": 0.0,
            "total_calories_kcal": 0.0
        }
    
    total_distance = db.query(func.sum(Activity.distance_m)).scalar() or 0
    total_duration = db.query(func.sum(Activity.duration_s)).scalar() or 0
    total_calories = db.query(func.sum(Activity.calories_kcal)).scalar() or 0
    
    return {
        "total_activities": total_activities,
        "total_distance_km": round(total_distance / 1000, 2),
        "total_duration_hours": round(total_duration / 3600, 2),
        "total_calories_kcal": round(total_calories, 0)
    }

@router.get("/trend", response_model=Dict[str, Any])
def get_stats_trend(db: Session = Depends(get_db)):
    """Get distance and count trends aggregated by month — computed at SQL level."""
    # Use strftime for SQLite, date_trunc for PostgreSQL  
    month_col = func.strftime("%Y-%m", Activity.start_time).label("month")
    
    results = db.query(
        month_col,
        func.sum(Activity.distance_m).label("total_distance"),
        func.count(Activity.id).label("count"),
        func.sum(Activity.duration_s).label("total_duration"),
    ).group_by(month_col).order_by(month_col).all()
    
    trends = [
        {
            "month": r.month,
            "distance_km": round((r.total_distance or 0) / 1000, 2),
            "count": r.count,
            "duration_hours": round((r.total_duration or 0) / 3600, 2),
        }
        for r in results
        if r.month  # skip null start_time rows
    ]
    
    return {"trends": trends}

@router.get("/distribution", response_model=Dict[str, Any])
def get_activity_distribution(db: Session = Depends(get_db)):
    """Get distribution of activity types."""
    distribution = db.query(
        Activity.activity_type, 
        func.count(Activity.id).label('count')
    ).group_by(Activity.activity_type).all()
    
    result = [{"type": d.activity_type or "Unknown", "count": d.count} for d in distribution]
    return {"distribution": result}
