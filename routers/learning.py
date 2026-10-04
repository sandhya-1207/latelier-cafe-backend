from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Subject, Topic, Subtopic
from schemas import SubjectResponse, TopicResponse
from typing import List

router = APIRouter(prefix="/api/learning", tags=["learning"])

@router.get("", response_model=List[SubjectResponse])
def get_all_learning_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).order_by(Subject.order.asc()).all()
    return subjects

@router.get("/subject/{slug}")
def get_subject_detail(slug: str, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.slug == slug).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    topics = db.query(Topic).filter(Topic.subject_id == subject.id).order_by(Topic.order.asc()).all()
    
    total_time = sum(t.time_spent_minutes for t in topics)
    avg_mastery = sum(t.mastery_percentage for t in topics) / len(topics) if topics else 0
    mastered_count = sum(1 for t in topics if t.status == "mastered")

    # Construct progressive learning path
    learning_path = []
    for idx, t in enumerate(topics):
        learning_path.append({
            "step": idx + 1,
            "id": t.id,
            "title": t.title,
            "slug": t.slug,
            "category": t.category,
            "status": t.status,
            "mastery": t.mastery_percentage,
            "difficulty": t.difficulty,
            "prerequisites": t.prerequisites
        })

    return {
        "id": subject.id,
        "slug": subject.slug,
        "title": subject.title,
        "description": subject.description,
        "icon": subject.icon,
        "color": subject.color,
        "stats": {
            "total_topics": len(topics),
            "mastered_topics": mastered_count,
            "avg_mastery": round(avg_mastery, 1),
            "total_hours": round(total_time / 60.0, 1)
        },
        "topics": topics,
        "learning_path": learning_path
    }
