from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import timedelta

from backend.core.config import settings, logger
from backend.core.database import get_db
from backend.models.activity import ImportRecord, Activity
from backend.utils.hash import calculate_bytes_hash
from backend.services.storage import save_uploaded_file
from backend.parsers.coros import CorosParser
from backend.parsers.huawei import HuaweiParser

router = APIRouter()

# FIT file magic bytes: ".FIT" at offset 8-11 (data size header is 12 bytes)
FIT_HEADER_MAGIC = b".FIT"
ALLOWED_EXTENSIONS = {'.fit', '.gpx', '.zip'}


def _validate_file(filename: str, content: bytes) -> None:
    """Validate file size and basic type checks."""
    # Size check
    if len(content) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(content) / (1024*1024):.1f}MB). "
                   f"Max allowed: {settings.MAX_UPLOAD_SIZE_MB}MB."
        )
    
    # Extension check
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # FIT magic number check
    if ext == '.fit' and len(content) >= 12:
        if FIT_HEADER_MAGIC not in content[8:12]:
            raise HTTPException(
                status_code=400,
                detail="File has .fit extension but does not appear to be a valid FIT file."
            )
    
    # Empty file check
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")


@router.post("/")
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    results = []
    
    for file in files:
        if not file.filename:
            continue
        
        logger.info("Processing upload: %s", file.filename)
            
        content = await file.read()
        
        # Validate file before processing
        try:
            _validate_file(file.filename, content)
        except HTTPException as e:
            logger.warning("File validation failed for %s: %s", file.filename, e.detail)
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": e.detail
            })
            continue
        
        file_hash = calculate_bytes_hash(content)
        
        # Check idempotency
        existing_record = db.query(ImportRecord).filter(ImportRecord.file_hash == file_hash).first()
        if existing_record and existing_record.status in ['success', 'skipped']:
            logger.info("Skipping duplicate file: %s (hash=%s)", file.filename, file_hash[:8])
            results.append({
                "filename": file.filename, 
                "status": "skipped", 
                "message": "File already imported successfully."
            })
            continue
        elif existing_record:
            # Delete the failed/stuck record so we can retry parsing
            db.delete(existing_record)
            db.commit()
            
        # Save raw file
        new_record = None
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
            
            logger.info("Upload success: %s — %d imported, %d skipped", file.filename, count, skipped)
            
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
            logger.error("Upload failed for %s: %s", file.filename, str(e))
            
            # Update the record indicating it failed parsing (if record was created)
            if new_record is not None:
                new_record.status = "failed"
                new_record.error_message = str(e)
                db.add(new_record)
                db.commit()
            
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": f"Parse error: {e}"
            })
            
    return {"results": results}
