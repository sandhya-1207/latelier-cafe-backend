from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Skill, SkillDependency

router = APIRouter(prefix="/api/skills", tags=["skills"])

@router.get("/graph")
def get_skills_graph(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    deps = db.query(SkillDependency).all()

    nodes = []
    category_colors = {
        "python": "#10b981", # emerald
        "math": "#6366f1",   # indigo
        "ml": "#8b5cf6",     # violet
        "cs": "#f59e0b",     # amber
        "systems": "#06b6d4" # cyan
    }

    for s in skills:
        nodes.append({
            "id": s.name,
            "name": s.name,
            "category": s.category,
            "level": s.level,
            "proficiency": s.proficiency,
            "importance": s.importance,
            "color": category_colors.get(s.category, "#94a3b8"),
            "radius": 18 + (s.importance * 3)
        })

    links = []
    for d in deps:
        links.append({
            "source": d.source_skill,
            "target": d.target_skill,
            "type": d.relationship_type
        })

    return {
        "nodes": nodes,
        "links": links,
        "categories": [
            {"id": "python", "label": "Python", "color": "#10b981"},
            {"id": "math", "label": "Mathematics", "color": "#6366f1"},
            {"id": "ml", "label": "Machine Learning", "color": "#8b5cf6"},
            {"id": "cs", "label": "Computer Science", "color": "#f59e0b"},
        ]
    }
