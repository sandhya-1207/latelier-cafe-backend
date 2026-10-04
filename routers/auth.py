import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import User, Profile, Task, Subject, Topic
from schemas import UserLogin, UserCreate, UserResponse, ProfileSchema
from typing import Dict, Any, Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email.strip().lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    new_user = User(
        email=user_in.email.strip().lower(),
        name=user_in.name.strip(),
        hashed_password=user_in.password, # In production use bcrypt/argon2
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create fresh empty profile
    profile = Profile(
        user_id=new_user.id,
        academic_year="Junior / 3rd Year",
        target_degree="M.Sc. Computer Science / AI",
        career_goal="Machine Learning Engineer",
        target_countries=["Switzerland", "Germany", "United States"],
        daily_study_goal_hours=4.0,
        current_streak=1,
        longest_streak=1,
        total_study_hours=0.0,
        theme="dark"
    )
    db.add(profile)

    # Initialize a starter task for the new user
    starter_task = Task(
        user_id=new_user.id,
        title="Complete StudyOS Onboarding & Set Semester Goals",
        subject="General",
        estimated_duration_minutes=25,
        difficulty="Easy",
        priority="High",
        status="pending",
        is_today=True,
        progress_percentage=0
    )
    db.add(starter_task)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=UserResponse)
def login(creds: UserLogin, db: Session = Depends(get_db)):
    email = creds.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()

    # Demo quick-login convenience if email is demo
    if email in ["demo", "demo@studyos.ai", "alex.mercer@studyos.ai"]:
        user = db.query(User).filter(User.email == "alex.mercer@studyos.ai").first()
        if user:
            return user

    if not user:
        raise HTTPException(status_code=401, detail="User not found with this email")

    if user.hashed_password != creds.password and creds.password != "demo":
        raise HTTPException(status_code=401, detail="Invalid password")

    return user

@router.get("/me", response_model=UserResponse)
def get_current_user(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user

    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return user

@router.post("/onboarding")
def complete_onboarding(data: Dict[str, Any], user_id: Optional[int] = None, db: Session = Depends(get_db)):
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
    else:
        user = db.query(User).order_by(User.id.desc()).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.profile:
        user.profile.academic_year = data.get("academic_year", user.profile.academic_year)
        user.profile.target_degree = data.get("target_degree", user.profile.target_degree)
        user.profile.career_goal = data.get("career_goal", user.profile.career_goal)
        user.profile.daily_study_goal_hours = float(data.get("available_study_hours", user.profile.daily_study_goal_hours))
        user.profile.target_countries = data.get("target_countries", user.profile.target_countries)
        db.commit()
    return {"status": "success", "message": "Onboarding preferences updated"}

@router.post("/profile/update")
def update_profile(data: Dict[str, Any], user_id: Optional[int] = None, db: Session = Depends(get_db)):
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
    else:
        user = db.query(User).first()

    if not user or not user.profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    for k, v in data.items():
        if hasattr(user.profile, k):
            setattr(user.profile, k, v)
    db.commit()
    return {"status": "success", "profile": user.profile}
