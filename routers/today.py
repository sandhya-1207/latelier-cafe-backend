import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task, StudySession, DailyPlan, User
from schemas import TaskCreate, TaskUpdate, StudySessionCreate
from typing import Dict, Any

router = APIRouter(prefix="/api/today", tags=["today"])

@router.get("")
def get_today_command_center(db: Session = Depends(get_db)):
    user = db.query(User).first()
    today_str = str(datetime.date.today())

    # Today's tasks
    tasks = db.query(Task).filter(Task.is_today == True).order_by(Task.completed_at.isnot(None), Task.id.asc()).all()

    # Today's completed sessions
    today_start = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    sessions = db.query(StudySession).filter(StudySession.completed_at >= today_start).order_by(StudySession.completed_at.desc()).all()

    # Daily plan / reflection
    plan = db.query(DailyPlan).filter(DailyPlan.date == today_str).first()
    if not plan:
        plan = db.query(DailyPlan).first()

    return {
        "date": today_str,
        "available_hours": plan.available_hours if plan else 4.5,
        "schedule_blocks": plan.schedule_blocks if plan else [],
        "tasks": tasks,
        "sessions": sessions,
        "total_study_minutes": sum(s.duration_minutes for s in sessions),
        "reflection": {
            "learned": plan.daily_reflection_learned if plan else "",
            "difficulty": plan.daily_reflection_difficulty if plan else "",
            "review": plan.daily_reflection_review if plan else "",
            "rating": plan.daily_rating if plan else 4
        }
    }

@router.post("/task")
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    user = db.query(User).first()
    new_task = Task(
        user_id=user.id,
        title=task_in.title,
        subject=task_in.subject,
        topic_id=task_in.topic_id,
        estimated_duration_minutes=task_in.estimated_duration_minutes,
        difficulty=task_in.difficulty,
        priority=task_in.priority,
        status="pending",
        is_today=True,
        progress_percentage=0,
        due_date=task_in.due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.patch("/task/{task_id}")
def update_task(task_id: int, updates: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = updates.model_dump(exclude_unset=True)
    for field, val in data.items():
        setattr(task, field, val)

    if updates.status == "completed" and not task.completed_at:
        task.completed_at = datetime.datetime.utcnow()
        task.progress_percentage = 100
    elif updates.status == "pending":
        task.completed_at = None

    db.commit()
    db.refresh(task)
    return task

@router.delete("/task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"status": "success", "message": "Task removed"}

@router.post("/reflection")
def save_reflection(data: Dict[str, Any], db: Session = Depends(get_db)):
    today_str = str(datetime.date.today())
    user = db.query(User).first()
    plan = db.query(DailyPlan).filter(DailyPlan.date == today_str).first()
    if not plan:
        plan = DailyPlan(user_id=user.id, date=today_str, schedule_blocks=[])
        db.add(plan)

    plan.daily_reflection_learned = data.get("learned", "")
    plan.daily_reflection_difficulty = data.get("difficulty", "")
    plan.daily_reflection_review = data.get("review", "")
    plan.daily_rating = int(data.get("rating", 4))
    db.commit()
    return {"status": "success", "message": "Daily reflection recorded"}
