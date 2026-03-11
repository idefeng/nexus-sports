from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import os
from datetime import timedelta

from backend.core.database import get_db
from backend.models.activity import ImportRecord, Activity
from backend.utils.hash import calculate_bytes_hash
from backend.services.storage import save_uploaded_file
from backend.parsers.coros import CorosParser
from backend.parsers.huawei import HuaweiParser

router = APIRouter()

@router.post("/")
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    results = []
    
    for file in files:
        if not file.filename:
            continue
            
        content = await file.read()
        file_hash = calculate_bytes_hash(content)
        
        # Check idempotency
        existing_record = db.query(ImportRecord).filter(ImportRecord.file_hash == file_hash).first()
        if existing_record:
            results.append({
                "filename": file.filename, 
                "status": "skipped", 
                "message": "File already imported."
            })
            continue
            
        # Save raw file
        try:
            saved_path = save_uploaded_file(content, file.filename)
            
            # Create import record
            new_record = ImportRecord(
                file_name=file.filename,
                file_hash=file_hash,
                status="processing",
                error_message=None
            )
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
            
            # Select Parser
            ext = os.path.splitext(file.filename)[1].lower()
            if ext in ['.fit', '.gpx']:
                parser = CorosParser()
            elif ext == '.zip':
                parser = HuaweiParser()
            else:
                raise Exception(f"Unsupported file format {ext}")
            
            # Parse activities
            parsed_activities = parser.parse(saved_path, file_hash)
            
            # Save to Database
            count = 0
            skipped = 0
            for act_create in parsed_activities:
                # Smart deduplication: check if an activity of the same type exists within +/- 5 minutes
                time_window = timedelta(minutes=5)
                existing_activity = db.query(Activity).filter(
                    Activity.activity_type == act_create.activity_type,
                    Activity.start_time >= act_create.start_time - time_window,
                    Activity.start_time <= act_create.start_time + time_window
                ).first()
                
                if existing_activity:
                    skipped += 1
                    continue
                    
                db_activity = Activity(**act_create.model_dump())
                db.add(db_activity)
                count += 1
            
            new_record.status = "success" if count > 0 else "skipped"
            if skipped > 0 and count == 0:
                new_record.status = "skipped"
                new_record.error_message = f"All {skipped} activities were duplicates."
            db.commit()
            
            status_msg = f"File processed. Imported {count} new activities."
            if skipped > 0:
                status_msg += f" Skipped {skipped} duplicates."
            
            results.append({
                "filename": file.filename,
                "status": "success" if count > 0 else "skipped",
                "record_id": new_record.id,
                "activities_imported": count,
                "activities_skipped": skipped,
                "message": status_msg
            })
            
        except Exception as e:
            db.rollback()
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })
            
    return {"results": results}
