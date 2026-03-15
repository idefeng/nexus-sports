from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from backend.core.database import get_db
from backend.models.activity import Activity
from backend.schemas.activity import ActivityResponse, ActivityUpdate

router = APIRouter()

@router.get("", response_model=Dict[str, Any])
def get_activities(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=1000, description="Max records to return"),
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    db: Session = Depends(get_db)
):
    """Get paginated list of activities."""
    query = db.query(Activity)
    
    if activity_type:
        query = query.filter(Activity.activity_type == activity_type)
    
    total = query.count()
    activities = query.order_by(Activity.start_time.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": [ActivityResponse.model_validate(a) for a in activities]
    }


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get a single activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """Delete a single activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(activity)
    db.commit()
    return {"status": "success", "message": f"Activity {activity_id} deleted."}


@router.patch("/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, payload: ActivityUpdate, db: Session = Depends(get_db)):
    """Partially update an activity (PATCH semantics)."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(activity, field):
            setattr(activity, field, value)

    db.commit()
    db.refresh(activity)
    return activity


@router.post("/maintenance/clear-all")
def clear_all_data(db: Session = Depends(get_db)):
    """Wipe all activity data and import records from the system."""
    from backend.models.activity import ImportRecord
    from backend.services.storage import clear_all_archives
    
    try:
        # Delete from DB
        db.query(Activity).delete()
        db.query(ImportRecord).delete()
        db.commit()
        
        # Delete from Filesystem
        clear_all_archives()
        
        return {"status": "success", "message": "All activity data cleared successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
