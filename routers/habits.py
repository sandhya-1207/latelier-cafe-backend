import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Habit, HabitLog, User
from schemas import HabitCreate
from typing import List, Dict, Any

router = APIRouter(prefix="/api/habits", tags=["habits"])

@router.get("")
def get_habits(db: Session = Depends(get_db)):
    habits = db.query(Habit).all()
    today = datetime.date.today()
    today_str = str(today)

    # Calculate past 7 days dates for weekly view
    week_dates = [(today - datetime.timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

    result = []
    for h in habits:
        logs_map = {l.date: l.completed for l in h.logs}
        week_status = [
            {"date": d, "completed": logs_map.get(d, False)}
            for d in week_dates
        ]
        completed_today = logs_map.get(today_str, False)
        result.append({
            "id": h.id,
            "name": h.name,
            "category": h.category,
            "frequency": h.frequency,
            "target_days_per_week": h.target_days_per_week,
            "current_streak": h.current_streak,
            "best_streak": h.best_streak,
            "color": h.color,
            "completed_today": completed_today,
            "week_status": week_status,
            "total_completed": len(h.logs)
        })
    return {
        "habits": result,
        "week_days": [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%a") for d in week_dates],
        "week_dates": week_dates
    }

@router.post("")
def create_habit(habit_in: HabitCreate, db: Session = Depends(get_db)):
    user = db.query(User).first()
    new_h = Habit(
        user_id=user.id,
        name=habit_in.name,
        category=habit_in.category,
        frequency=habit_in.frequency,
        target_days_per_week=habit_in.target_days_per_week,
        color=habit_in.color,
        current_streak=0,
        best_streak=0
    )
    db.add(new_h)
    db.commit()
    db.refresh(new_h)
    return new_h

@router.post("/{habit_id}/toggle")
def toggle_habit_date(habit_id: int, data: Dict[str, Any] = {}, db: Session = Depends(get_db)):
    target_date = data.get("date", str(datetime.date.today()))
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    existing_log = db.query(HabitLog).filter(HabitLog.habit_id == habit_id, HabitLog.date == target_date).first()
    if existing_log:
        existing_log.completed = not existing_log.completed
        is_completed = existing_log.completed
    else:
        new_log = HabitLog(habit_id=habit_id, date=target_date, completed=True, value=1.0)
        db.add(new_log)
        is_completed = True

    # Adjust streak if toggling today
    if target_date == str(datetime.date.today()):
        if is_completed:
            habit.current_streak += 1
            if habit.current_streak > habit.best_streak:
                habit.best_streak = habit.current_streak
        else:
            habit.current_streak = max(0, habit.current_streak - 1)

    db.commit()
    return {"status": "success", "completed": is_completed, "streak": habit.current_streak}
