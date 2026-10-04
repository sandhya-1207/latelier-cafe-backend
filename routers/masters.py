from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import University, Program, Application, Document, User
from schemas import UniversityResponse, ApplicationResponse
from typing import List, Dict, Any

router = APIRouter(prefix="/api/masters", tags=["masters"])

@router.get("/universities", response_model=List[UniversityResponse])
def get_universities(db: Session = Depends(get_db)):
    return db.query(University).order_by(University.ranking_cs.asc()).all()

@router.get("/applications", response_model=List[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return db.query(Application).all()

@router.get("/pipeline")
def get_application_pipeline(db: Session = Depends(get_db)):
    apps = db.query(Application).all()
    stages = ["Researching", "Shortlisted", "Preparing", "Applied", "Interview", "Accepted", "Rejected"]
    pipeline = {stage: [] for stage in stages}

    for a in apps:
        stage = a.status if a.status in pipeline else "Researching"
        docs_ready = sum(1 for d in a.documents if d.status in ["Ready", "Submitted"])
        docs_total = len(a.documents)
        pipeline[stage].append({
            "id": a.id,
            "university_id": a.university_id,
            "university_name": a.university.name if a.university else "",
            "short_name": a.university.short_name if a.university else "",
            "country": a.university.country if a.university else "",
            "ranking_cs": a.university.ranking_cs if a.university else 99,
            "program_name": a.program.name if a.program else "",
            "tier": a.tier,
            "status": a.status,
            "deadline": a.deadline.strftime("%b %d, %Y") if a.deadline else "Rolling",
            "tuition_eur": a.university.tuition_eur if a.university else 0,
            "docs_ready": docs_ready,
            "docs_total": docs_total,
            "notes": a.notes
        })
    return pipeline

@router.post("/applications/{app_id}/status")
def update_application_status(app_id: int, data: Dict[str, Any], db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    new_status = data.get("status")
    if new_status:
        app.status = new_status
    if "tier" in data:
        app.tier = data["tier"]
    if "notes" in data:
        app.notes = data["notes"]

    db.commit()
    return {"status": "success", "app_id": app.id, "new_status": app.status}

@router.post("/applications/{app_id}/documents/{doc_id}/status")
def update_document_status(app_id: int, doc_id: int, data: Dict[str, Any], db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id, Document.application_id == app_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if "status" in data:
        doc.status = data["status"]
    if "notes" in data:
        doc.notes = data["notes"]

    db.commit()
    return {"status": "success", "doc_id": doc.id, "new_status": doc.status}
