from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
import os
import io

from backend.core.database import get_db
from backend.core.config import settings
from backend.models.activity import Activity, ImportRecord

import gpxpy
import gpxpy.gpx
import polyline

router = APIRouter()

@router.get("/original/{activity_id}")
def get_original_file(activity_id: int, db: Session = Depends(get_db)):
    """Download the original archived file for a given activity."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
        
    if not activity.original_file_hash:
        raise HTTPException(status_code=404, detail="No original file associated with this activity")
        
    # Find the filename from the import record
    import_record = db.query(ImportRecord).filter(ImportRecord.file_hash == activity.original_file_hash).first()
    if not import_record or not import_record.file_name:
        raise HTTPException(status_code=404, detail="Original filename not found in records")
        
    file_path = os.path.join(settings.ARCHIVE_DIR, import_record.file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Original file not found on disk")
        
    return FileResponse(
        path=file_path, 
        filename=import_record.file_name,
        media_type='application/octet-stream'
    )

@router.get("/gpx/{activity_id}")
def get_gpx_export(activity_id: int, db: Session = Depends(get_db)):
    """Generate and download a basic GPX file from the saved polyline."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
        
    if not activity.polyline:
        raise HTTPException(status_code=404, detail="No GPS track available for this activity")
        
    try:
        coordinates = polyline.decode(activity.polyline)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to decode polyline: {e}")
        
    gpx = gpxpy.gpx.GPX()
    
    # Create first track in our GPX
    gpx_track = gpxpy.gpx.GPXTrack(name=f"{activity.activity_type} - {activity.start_time.strftime('%Y-%m-%d')}")
    gpx.tracks.append(gpx_track)
    
    # Create first segment in our GPX track
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    
    # Approximate timing for points based on total duration
    # Since we only have compressed polyline without individual point timestamps,
    # we simulate an average pace distribution
    num_points = len(coordinates)
    
    start_time = activity.start_time
    duration_per_point = activity.duration_s / max(num_points, 1) if activity.duration_s else 0
    
    from datetime import timedelta
    
    current_time = start_time
    for lat, lon in coordinates:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
            latitude=lat, 
            longitude=lon, 
            time=current_time
        ))
        if current_time:
            current_time += timedelta(seconds=duration_per_point)
            
    xml_str = gpx.to_xml()
    
    export_filename = f"nexus_sports_{activity.id}_{activity.start_time.strftime('%Y%m%d')}.gpx"
    
    return Response(
        content=xml_str,
        media_type="application/gpx+xml",
        headers={"Content-Disposition": f"attachment; filename={export_filename}"}
    )
