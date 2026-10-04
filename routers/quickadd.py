import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task, StudySession, Note, Habit, Project, Goal, User
from typing import Dict, Any

router = APIRouter(prefix="/api/quickadd", tags=["quickadd"])

@router.post("")
def handle_quick_add(data: Dict[str, Any], db: Session = Depends(get_db)):
    user = db.query(User).first()
    item_type = data.get("type", "task")
    title = data.get("title", "").strip()

    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    if item_type == "task":
        new_task = Task(
            user_id=user.id,
            title=title,
            subject=data.get("subject", "General"),
            estimated_duration_minutes=int(data.get("duration", 45)),
            difficulty=data.get("difficulty", "Medium"),
            priority=data.get("priority", "Medium"),
            status="pending",
            is_today=True
        )
        db.add(new_task)
        db.commit()
        return {"status": "success", "type": "task", "id": new_task.id, "message": f"Task '{title}' added to Today"}

    elif item_type == "session":
        new_session = StudySession(
            user_id=user.id,
            subject=data.get("subject", "General"),
            topic=title,
            duration_minutes=int(data.get("duration", 30)),
            session_type="pomodoro",
            focus_score=95.0,
            completed_at=datetime.datetime.utcnow()
        )
        db.add(new_session)
        db.commit()
        return {"status": "success", "type": "session", "id": new_session.id, "message": "Study session logged"}

    elif item_type == "note":
        new_note = Note(
            user_id=user.id,
            title=title,
            content=data.get("content", ""),
            tags=data.get("tags", ["Quick Note"])
        )
        db.add(new_note)
        db.commit()
        return {"status": "success", "type": "note", "id": new_note.id, "message": "Note saved"}

    elif item_type == "habit":
        new_habit = Habit(
            user_id=user.id,
            name=title,
            category=data.get("category", "Study"),
            frequency="daily",
            target_days_per_week=7,
            color="indigo"
        )
        db.add(new_habit)
        db.commit()
        return {"status": "success", "type": "habit", "id": new_habit.id, "message": "Habit created"}

    elif item_type == "goal":
        new_goal = Goal(
            user_id=user.id,
            title=title,
            description=data.get("description", ""),
            level="monthly",
            progress=0.0
        )
        db.add(new_goal)
        db.commit()
        return {"status": "success", "type": "goal", "id": new_goal.id, "message": "Goal established"}

    else:
        raise HTTPException(status_code=400, detail="Invalid quick-add item type")
