import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import StudySession, User
from schemas import StudySessionCreate, StudySessionResponse

router = APIRouter(prefix="/api/focus", tags=["focus"])

@router.get("/sessions", response_model=list[StudySessionResponse])
def get_focus_sessions(db: Session = Depends(get_db)):
    return db.query(StudySession).order_by(StudySession.completed_at.desc()).limit(20).all()

@router.post("/session")
def record_focus_session(session_in: StudySessionCreate, db: Session = Depends(get_db)):
    user = db.query(User).first()
    new_s = StudySession(
        user_id=user.id,
        subject=session_in.subject,
        topic=session_in.topic,
        duration_minutes=session_in.duration_minutes,
        session_type=session_in.session_type,
        notes=session_in.notes or "",
        focus_score=session_in.focus_score,
        completed_at=datetime.datetime.utcnow()
    )
    db.add(new_s)

    # Increment user total study hours
    if user and user.profile:
        user.profile.total_study_hours = round(user.profile.total_study_hours + (session_in.duration_minutes / 60.0), 2)

    db.commit()
    db.refresh(new_s)
    return new_s
