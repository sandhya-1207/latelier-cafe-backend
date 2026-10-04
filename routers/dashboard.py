import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import (
    User, Subject, Topic, Task, StudySession, Goal,
    Habit, HabitLog, CodingProblem, Project, AIRecommendation
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("")
def get_dashboard_data(db: Session = Depends(get_db)):
    user = db.query(User).first()
    profile = user.profile if user else None

    # Streak & stats
    streak = profile.current_streak if profile else 14
    total_hours = profile.total_study_hours if profile else 216.5
    weekly_goal_hours = 25.0
    
    # Calculate study time today
    today_start = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_sessions = db.query(StudySession).filter(StudySession.completed_at >= today_start).all()
    today_study_minutes = sum(s.duration_minutes for s in today_sessions)

    # Today's active tasks
    today_tasks = db.query(Task).filter(Task.is_today == True).order_by(Task.status.desc(), Task.id.asc()).all()

    # Continue learning (recently studied topics)
    recent_topics = db.query(Topic).order_by(Topic.last_studied_at.desc().nullslast()).limit(4).all()

    # Skill overview metrics
    subjects = db.query(Subject).all()
    skill_overview = []
    for sub in subjects:
        top_list = sub.topics
        avg_mastery = sum(t.mastery_percentage for t in top_list) / len(top_list) if top_list else 0
        total_time = sum(t.time_spent_minutes for t in top_list)
        skill_overview.append({
            "subject_id": sub.id,
            "slug": sub.slug,
            "title": sub.title,
            "color": sub.color,
            "icon": sub.icon,
            "topics_count": len(top_list),
            "mastery_percentage": round(avg_mastery, 1),
            "time_spent_hours": round(total_time / 60, 1)
        })

    # AI Recommendation (highest priority active recommendation)
    top_recommendation = db.query(AIRecommendation).filter(AIRecommendation.is_dismissed == False).order_by(AIRecommendation.priority_score.desc()).first()

    # Weekly contribution heatmap (last 7 days study hours)
    weekly_activity = []
    today = datetime.date.today()
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        day_start = datetime.datetime.combine(day, datetime.time.min)
        day_end = datetime.datetime.combine(day, datetime.time.max)
        sessions = db.query(StudySession).filter(StudySession.completed_at >= day_start, StudySession.completed_at <= day_end).all()
        hours = sum(s.duration_minutes for s in sessions) / 60.0
        weekly_activity.append({
            "date": day.strftime("%a"),
            "full_date": str(day),
            "hours": round(hours, 1),
            "intensity": min(4, int(hours * 1.5))
        })

    # Coding snapshot
    total_problems = db.query(CodingProblem).count()
    solved_problems = db.query(CodingProblem).filter(CodingProblem.solved == True).count()

    # Active projects
    active_projects = db.query(Project).filter(Project.status != "deployed").limit(3).all()

    return {
        "user": {
            "name": user.name if user else "Alex Mercer",
            "career_goal": profile.career_goal if profile else "Machine Learning Research Engineer",
            "academic_year": profile.academic_year if profile else "Senior Undergrad",
            "current_streak": streak,
            "total_study_hours": total_hours,
            "today_study_hours": round(today_study_minutes / 60.0, 1),
            "weekly_goal_hours": weekly_goal_hours,
            "weekly_progress_pct": min(100, int((sum(d["hours"] for d in weekly_activity) / weekly_goal_hours) * 100))
        },
        "today_tasks": today_tasks,
        "continue_learning": [
            {
                "id": t.id,
                "title": t.title,
                "category": t.category,
                "subject": t.subject.title if t.subject else "",
                "subject_slug": t.subject.slug if t.subject else "",
                "difficulty": t.difficulty,
                "mastery_percentage": t.mastery_percentage,
                "time_spent_minutes": t.time_spent_minutes,
                "status": t.status
            }
            for t in recent_topics
        ],
        "skill_overview": skill_overview,
        "ai_recommendation": top_recommendation,
        "weekly_activity": weekly_activity,
        "coding_snapshot": {
            "total": total_problems,
            "solved": solved_problems,
            "accuracy_pct": 89
        },
        "active_projects": [
            {
                "id": p.id,
                "title": p.title,
                "status": p.status,
                "progress": p.progress,
                "technologies": p.technologies
            }
            for p in active_projects
        ]
    }
