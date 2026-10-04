import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Topic, Subtopic, Note, User
from schemas import TopicResponse
from typing import Dict, Any

router = APIRouter(prefix="/api/topics", tags=["topics"])

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic_detail(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("/{topic_id}/subtopic/{subtopic_id}/toggle")
def toggle_subtopic(topic_id: int, subtopic_id: int, db: Session = Depends(get_db)):
    subtopic = db.query(Subtopic).filter(Subtopic.id == subtopic_id, Subtopic.topic_id == topic_id).first()
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")

    subtopic.is_completed = not subtopic.is_completed
    db.commit()

    # Recalculate topic progress
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    all_sub = topic.subtopics
    if all_sub:
        comp = sum(1 for s in all_sub if s.is_completed)
        topic.mastery_percentage = round((comp / len(all_sub)) * 100, 1)
        if topic.mastery_percentage >= 90:
            topic.status = "mastered"
        elif topic.mastery_percentage > 0:
            topic.status = "in_progress"
        db.commit()

    return {"status": "success", "is_completed": subtopic.is_completed, "topic_mastery": topic.mastery_percentage}

@router.post("/{topic_id}/mastery")
def update_topic_mastery(topic_id: int, data: Dict[str, Any], db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    if "theory_mastery" in data:
        topic.theory_mastery = float(data["theory_mastery"])
    if "math_mastery" in data:
        topic.math_mastery = float(data["math_mastery"])
    if "impl_mastery" in data:
        topic.impl_mastery = float(data["impl_mastery"])
    if "status" in data:
        topic.status = data["status"]

    topic.mastery_percentage = round((topic.theory_mastery + topic.math_mastery + topic.impl_mastery) / 3.0, 1)
    topic.last_studied_at = datetime.datetime.utcnow()
    db.commit()
    return {"status": "success", "mastery_percentage": topic.mastery_percentage, "status": topic.status}

@router.post("/{topic_id}/notes")
def add_topic_note(topic_id: int, data: Dict[str, Any], db: Session = Depends(get_db)):
    user = db.query(User).first()
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    note = Note(
        user_id=user.id,
        topic_id=topic_id,
        title=data.get("title", f"Notes on {topic.title}"),
        content=data.get("content", ""),
        tags=data.get("tags", [topic.category])
    )
    db.add(note)
    db.commit()
    return {"status": "success", "note_id": note.id}
