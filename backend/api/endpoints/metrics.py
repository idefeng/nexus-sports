from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.models.metrics import BodyMetrics
from backend.schemas.metrics import BodyMetricsCreate, BodyMetricsRead, BodyMetricsUpdate

router = APIRouter()

@router.post("/", response_model=BodyMetricsRead)
def create_metrics(metrics: BodyMetricsCreate, db: Session = Depends(get_db)):
    db_metrics = BodyMetrics(**metrics.model_dump())
    db.add(db_metrics)
    db.commit()
    db.refresh(db_metrics)
    return db_metrics

@router.get("/", response_model=List[BodyMetricsRead])
def read_metrics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    metrics = db.query(BodyMetrics).order_by(BodyMetrics.recorded_at.desc()).offset(skip).limit(limit).all()
    return metrics

@router.get("/latest", response_model=BodyMetricsRead)
def read_latest_metrics(db: Session = Depends(get_db)):
    metrics = db.query(BodyMetrics).order_by(BodyMetrics.recorded_at.desc()).first()
    if not metrics:
        raise HTTPException(status_code=404, detail="No metrics found")
    return metrics

@router.delete("/{metrics_id}")
def delete_metrics(metrics_id: int, db: Session = Depends(get_db)):
    db_metrics = db.query(BodyMetrics).filter(BodyMetrics.id == metrics_id).first()
    if not db_metrics:
        raise HTTPException(status_code=404, detail="Metrics not found")
    db.delete(db_metrics)
    db.commit()
    return {"status": "success"}
