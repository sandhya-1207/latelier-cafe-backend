from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Project, Milestone, ProjectTask, User
from schemas import ProjectResponse
from typing import List, Dict, Any

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.get("", response_model=List[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("")
def create_project(data: Dict[str, Any], db: Session = Depends(get_db)):
    user = db.query(User).first()
    new_proj = Project(
        user_id=user.id,
        title=data.get("title", "New Project"),
        description=data.get("description", ""),
        status="planning",
        progress=0.0,
        github_url=data.get("github_url", ""),
        technologies=data.get("technologies", ["Python"]),
        cover_style=data.get("cover_style", "neural-mesh")
    )
    db.add(new_proj)
    db.commit()
    db.refresh(new_proj)

    # Add default standard milestones
    milestones = [
        Milestone(project_id=new_proj.id, title="1. Architecture & Formal Problem Formulation", phase="Planning", is_completed=False, order=1),
        Milestone(project_id=new_proj.id, title="2. Mathematical Derivations & Data Ingestion", phase="Research", is_completed=False, order=2),
        Milestone(project_id=new_proj.id, title="3. Core Model Implementation", phase="Development", is_completed=False, order=3),
        Milestone(project_id=new_proj.id, title="4. Unit Testing & Performance Benchmarks", phase="Testing", is_completed=False, order=4),
        Milestone(project_id=new_proj.id, title="5. Technical Documentation & Deployment", phase="Deployment", is_completed=False, order=5),
    ]
    db.add_all(milestones)
    db.commit()
    return new_proj

@router.post("/{project_id}/milestones/{milestone_id}/toggle")
def toggle_milestone(project_id: int, milestone_id: int, db: Session = Depends(get_db)):
    ms = db.query(Milestone).filter(Milestone.id == milestone_id, Milestone.project_id == project_id).first()
    if not ms:
        raise HTTPException(status_code=404, detail="Milestone not found")

    ms.is_completed = not ms.is_completed
    db.commit()

    # Recalculate project progress
    proj = db.query(Project).filter(Project.id == project_id).first()
    all_ms = proj.milestones
    if all_ms:
        comp = sum(1 for m in all_ms if m.is_completed)
        proj.progress = round((comp / len(all_ms)) * 100, 1)
        if proj.progress == 100:
            proj.status = "deployed"
        elif proj.progress >= 75:
            proj.status = "testing"
        elif proj.progress >= 25:
            proj.status = "development"
        db.commit()

    return {"status": "success", "is_completed": ms.is_completed, "progress": proj.progress}

@router.post("/{project_id}/tasks/{task_id}/toggle")
def toggle_project_task(project_id: int, task_id: int, db: Session = Depends(get_db)):
    pt = db.query(ProjectTask).filter(ProjectTask.id == task_id, ProjectTask.project_id == project_id).first()
    if not pt:
        raise HTTPException(status_code=404, detail="Project task not found")
    pt.completed = not pt.completed
    db.commit()
    return {"status": "success", "completed": pt.completed}
