from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import calendar

from backend.core.database import get_db
from backend.models.activity import Activity

router = APIRouter()

@router.get("/latest_activity")
def get_latest_activity(db: Session = Depends(get_db)):
    """Returns a natural language summary of the most recent activity."""
    act = db.query(Activity).order_by(Activity.start_time.desc()).first()
    
    if not act:
        return {"status": "success", "report": "目前系统中还没有任何运动记录。"}
        
    date_str = act.start_time.strftime("%Y年%m月%d日 %H:%M")
    distance_km = act.distance_m / 1000 if act.distance_m else 0
    duration_min = act.duration_s / 60 if act.duration_s else 0
    
    report = f"您最近一次运动是在 {date_str}，进行了一次 {act.activity_type}。"
    report += f" 总共前进了 {distance_km:.2f} 公里，历时 {duration_min:.1f} 分钟。"
    
    if act.avg_heart_rate:
        report += f" 平均心率为 {act.avg_heart_rate:.0f} bpm。"
    if act.calories_kcal:
        report += f" 消耗了约 {act.calories_kcal:.0f} 千卡热量。"
        
    return {
        "status": "success",
        "activity_id": act.id,
        "report": report,
        "raw_data": {
            "type": act.activity_type,
            "distance_m": act.distance_m,
            "duration_s": act.duration_s
        }
    }

@router.get("/monthly_report")
def get_monthly_report(target_month: str = None, db: Session = Depends(get_db)):
    """
    Returns an aggregated monthly report. 
    target_month: YYYY-MM format. Defaults to current month if not provided.
    """
    if not target_month:
        now = datetime.now()
        target_month = now.strftime("%Y-%m")
        
    try:
        year, month = map(int, target_month.split('-'))
        # Get start and end of the month
        _, last_day = calendar.monthrange(year, month)
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, last_day, 23, 59, 59)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid target_month format. Use YYYY-MM")

    activities = db.query(Activity).filter(
        Activity.start_time >= start_date,
        Activity.start_time <= end_date
    ).all()
    
    if not activities:
        return {
            "status": "success", 
            "report": f"您在 {target_month} 没有记录任何运动。"
        }
        
    total_count = len(activities)
    total_distance_m = sum(a.distance_m for a in activities if a.distance_m)
    total_duration_s = sum(a.duration_s for a in activities if a.duration_s)
    
    # Calculate most frequent activity type
    types = [a.activity_type for a in activities]
    favorite_type = max(set(types), key=types.count) if types else "未知"
    
    report = f"【{target_month} 运动月报】\n"
    report += f"本月您总共完成了 {total_count} 次运动，最常进行的运动是 {favorite_type}。\n"
    report += f"累计里程达到了 {total_distance_m/1000:.2f} 公里，总运动时长为 {total_duration_s/3600:.1f} 小时。"
    
    return {
        "status": "success",
        "month": target_month,
        "report": report,
        "metrics": {
            "total_count": total_count,
            "total_distance_km": round(total_distance_m/1000, 2),
            "total_duration_hours": round(total_duration_s/3600, 2),
            "favorite_type": favorite_type
        }
    }
