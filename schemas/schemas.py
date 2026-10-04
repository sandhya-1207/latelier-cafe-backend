from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import datetime

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ProfileSchema(BaseModel):
    academic_year: str
    target_degree: str
    career_goal: str
    target_countries: List[str]
    daily_study_goal_hours: float
    current_streak: int
    longest_streak: int
    total_study_hours: float
    avatar_url: str
    theme: str

    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    created_at: datetime.datetime
    profile: Optional[ProfileSchema] = None

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    subject: str = "General"
    topic_id: Optional[int] = None
    estimated_duration_minutes: int = 45
    difficulty: str = "Medium"
    priority: str = "Medium"
    status: str = "pending"
    is_today: bool = True
    progress_percentage: int = 0
    due_date: Optional[datetime.datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    topic_id: Optional[int] = None
    estimated_duration_minutes: Optional[int] = None
    difficulty: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    is_today: Optional[bool] = None
    progress_percentage: Optional[int] = None
    due_date: Optional[datetime.datetime] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class StudySessionCreate(BaseModel):
    subject: str
    topic: str = ""
    duration_minutes: int
    session_type: str = "pomodoro"
    notes: Optional[str] = ""
    focus_score: float = 90.0

class StudySessionResponse(StudySessionCreate):
    id: int
    completed_at: datetime.datetime

    class Config:
        from_attributes = True

class SubtopicResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    understanding_score: float
    notes: str

    class Config:
        from_attributes = True

class TopicResponse(BaseModel):
    id: int
    subject_id: int
    title: str
    slug: str
    description: str
    category: str
    difficulty: str
    status: str
    mastery_percentage: float
    theory_mastery: float
    math_mastery: float
    impl_mastery: float
    time_spent_minutes: int
    problems_solved: int
    last_studied_at: Optional[datetime.datetime] = None
    prerequisites: List[Any] = []
    related_topics: List[Any] = []
    ml_applications: List[Any] = []
    subtopics: List[SubtopicResponse] = []

    class Config:
        from_attributes = True

class SubjectResponse(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    icon: str
    color: str
    order: int
    topics: List[TopicResponse] = []

    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    title: str
    description: str = ""
    level: str = "yearly"
    parent_goal_id: Optional[int] = None
    target_date: Optional[datetime.datetime] = None
    progress: float = 0.0
    status: str = "active"

class GoalCreate(GoalBase):
    pass

class GoalResponse(GoalBase):
    id: int
    sub_goals: List[Any] = []

    class Config:
        from_attributes = True

class HabitBase(BaseModel):
    name: str
    category: str = "Study"
    frequency: str = "daily"
    target_days_per_week: int = 7
    color: str = "emerald"

class HabitCreate(HabitBase):
    pass

class HabitLogResponse(BaseModel):
    id: int
    date: str
    completed: bool
    value: float

    class Config:
        from_attributes = True

class HabitResponse(HabitBase):
    id: int
    current_streak: int
    best_streak: int
    logs: List[HabitLogResponse] = []

    class Config:
        from_attributes = True

class MilestoneResponse(BaseModel):
    id: int
    title: str
    phase: str
    is_completed: bool
    target_date: Optional[datetime.datetime] = None
    order: int

    class Config:
        from_attributes = True

class ProjectTaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    due_date: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    progress: float
    deadline: Optional[datetime.datetime] = None
    github_url: str
    demo_url: str
    technologies: List[str] = []
    cover_style: str
    tasks: List[ProjectTaskResponse] = []
    milestones: List[MilestoneResponse] = []

    class Config:
        from_attributes = True

class CodingProblemResponse(BaseModel):
    id: int
    title: str
    platform: str
    platform_problem_id: str
    difficulty: str
    category: str
    tags: List[str] = []
    url: str
    solved: bool
    solve_time_minutes: int
    attempts: int
    notes: str
    last_attempted_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class UniversityResponse(BaseModel):
    id: int
    name: str
    short_name: str
    country: str
    city: str
    ranking_world: int
    ranking_cs: int
    tuition_eur: float
    semester_contribution_eur: float
    website: str
    logo_letter: str
    cover_image_key: str
    description: str

    class Config:
        from_attributes = True

class ProgramResponse(BaseModel):
    id: int
    university_id: int
    name: str
    degree: str
    duration_semesters: int
    language: str
    application_deadline: str
    gpa_requirement: str
    gre_requirement: str
    language_requirement: str
    scholarship_opportunities: str
    credits_ects: int

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: int
    name: str
    status: str
    file_path: str
    notes: str

    class Config:
        from_attributes = True

class ApplicationResponse(BaseModel):
    id: int
    university_id: int
    program_id: Optional[int] = None
    status: str
    tier: str
    deadline: Optional[datetime.datetime] = None
    portal_url: str
    application_fee_eur: float
    notes: str
    university: Optional[UniversityResponse] = None
    program: Optional[ProgramResponse] = None
    documents: List[DocumentResponse] = []

    class Config:
        from_attributes = True

class AIPlannerRequest(BaseModel):
    available_hours: float = 3.0
    focus_preference: Optional[str] = "balanced" # balanced, math_heavy, ml_heavy, coding_heavy
    notes: Optional[str] = ""

class DailyScheduleItem(BaseModel):
    time: str
    duration_minutes: int
    subject: str
    topic: str
    type: str # theory, practice, coding, review
    reason: str
    difficulty: str

class AIPlannerResponse(BaseModel):
    date: str
    available_hours: float
    schedule: List[DailyScheduleItem]
    insights: str

class AIChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class AIChatResponse(BaseModel):
    reply: str
    suggested_actions: Optional[List[Dict[str, str]]] = []
