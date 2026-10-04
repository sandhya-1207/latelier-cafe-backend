from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Goal, User
from schemas import GoalResponse, GoalCreate
from typing import List, Dict, Any

router = APIRouter(prefix="/api/goals", tags=["goals"])

@router.get("", response_model=List[GoalResponse])
def get_all_goals(db: Session = Depends(get_db)):
    # Return top-level goals with nested sub-goals
    return db.query(Goal).filter(Goal.parent_goal_id.is_(None)).all()

@router.get("/hierarchy")
def get_goal_hierarchy(db: Session = Depends(get_db)):
    all_goals = db.query(Goal).all()
    # Group by level
    levels = {
        "long_term": [],
        "yearly": [],
        "quarterly": [],
        "monthly": [],
        "weekly": [],
        "daily": []
    }
    for g in all_goals:
        if g.level in levels:
            levels[g.level].append({
                "id": g.id,
                "title": g.title,
                "description": g.description,
                "progress": g.progress,
                "status": g.status,
                "parent_id": g.parent_goal_id
            })
    return levels

@router.post("")
def create_goal(goal_in: GoalCreate, db: Session = Depends(get_db)):
    user = db.query(User).first()
    new_g = Goal(
        user_id=user.id,
        title=goal_in.title,
        description=goal_in.description,
        level=goal_in.level,
        parent_goal_id=goal_in.parent_goal_id,
        progress=goal_in.progress,
        status=goal_in.status
    )
    db.add(new_g)
    db.commit()
    db.refresh(new_g)
    return new_g

@router.patch("/{goal_id}")
def update_goal(goal_id: int, data: Dict[str, Any], db: Session = Depends(get_db)):
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    for k, v in data.items():
        if hasattr(goal, k):
            setattr(goal, k, v)
    db.commit()
    db.refresh(goal)
    return goal
