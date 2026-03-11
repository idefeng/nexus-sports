from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from datetime import datetime, timedelta

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
    """Get distance trends aggregated by month."""
    activities = db.query(Activity.start_time, Activity.distance_m).all()
    
    # Process grouping in Python for SQLite compatibility
    trends = {}
    for start_time, distance in activities:
        if start_time and distance:
            month_key = start_time.strftime("%Y-%m")
            trends[month_key] = trends.get(month_key, 0) + (distance / 1000)
            
    # Sort by month
    sorted_trends = [{"month": k, "distance_km": round(v, 2)} for k, v in sorted(trends.items())]
    
    return {"trends": sorted_trends}

@router.get("/distribution", response_model=Dict[str, Any])
def get_activity_distribution(db: Session = Depends(get_db)):
    """Get distribution of activity types."""
    distribution = db.query(
        Activity.activity_type, 
        func.count(Activity.id).label('count')
    ).group_by(Activity.activity_type).all()
    
    result = [{"type": d.activity_type or "Unknown", "count": d.count} for d in distribution]
    return {"distribution": result}
