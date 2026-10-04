import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("StudySession", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    coding_attempts = relationship("CodingAttempt", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    daily_plans = relationship("DailyPlan", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    academic_year = Column(String(50), default="Junior / 3rd Year")
    target_degree = Column(String(100), default="M.Sc. Computer Science / AI")
    career_goal = Column(String(255), default="Machine Learning Research Engineer")
    target_countries = Column(JSON, default=lambda: ["Switzerland", "Germany", "United States", "United Kingdom"])
    daily_study_goal_hours = Column(Float, default=4.0)
    current_streak = Column(Integer, default=14)
    longest_streak = Column(Integer, default=26)
    total_study_hours = Column(Float, default=184.5)
    avatar_url = Column(String(500), default="")
    theme = Column(String(20), default="dark")

    user = relationship("User", back_populates="profile")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, default="")
    icon = Column(String(50), default="book")
    color = Column(String(20), default="indigo")
    order = Column(Integer, default=0)

    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(100), index=True, nullable=False)
    description = Column(Text, default="")
    category = Column(String(100), default="Core")
    difficulty = Column(String(20), default="Intermediate") # Beginner, Intermediate, Advanced
    status = Column(String(20), default="in_progress") # not_started, in_progress, mastered, review
    mastery_percentage = Column(Float, default=0.0) # 0-100
    theory_mastery = Column(Float, default=0.0)
    math_mastery = Column(Float, default=0.0)
    impl_mastery = Column(Float, default=0.0)
    time_spent_minutes = Column(Integer, default=0)
    problems_solved = Column(Integer, default=0)
    last_studied_at = Column(DateTime, nullable=True)
    order = Column(Integer, default=0)
    prerequisites = Column(JSON, default=list) # list of topic titles/ids
    related_topics = Column(JSON, default=list)
    ml_applications = Column(JSON, default=list)

    subject = relationship("Subject", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="topic")

class Subtopic(Base):
    __tablename__ = "subtopics"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False)
    understanding_score = Column(Float, default=0.0) # 0 to 5.0
    notes = Column(Text, default="")

    topic = relationship("Topic", back_populates="subtopics")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False) # python, math, ml, cs, systems
    level = Column(String(20), default="Intermediate")
    proficiency = Column(Float, default=50.0) # 0-100
    importance = Column(Integer, default=3) # 1-5

class SkillDependency(Base):
    __tablename__ = "skill_dependencies"

    id = Column(Integer, primary_key=True, index=True)
    source_skill = Column(String(100), nullable=False)
    target_skill = Column(String(100), nullable=False)
    relationship_type = Column(String(50), default="prerequisite") # prerequisite, foundation, co_requisite

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    subject = Column(String(100), default="General")
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    estimated_duration_minutes = Column(Integer, default=45)
    difficulty = Column(String(20), default="Medium") # Easy, Medium, Hard
    priority = Column(String(20), default="Medium") # Low, Medium, High, Urgent
    status = Column(String(20), default="pending") # pending, in_progress, completed
    due_date = Column(DateTime, nullable=True)
    is_today = Column(Boolean, default=True)
    progress_percentage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="tasks")

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    topic = Column(String(255), default="")
    duration_minutes = Column(Integer, default=25)
    session_type = Column(String(50), default="pomodoro") # pomodoro, stopwatch, deep_work
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(Text, default="")
    focus_score = Column(Float, default=90.0) # 0-100

    user = relationship("User", back_populates="sessions")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    level = Column(String(30), default="yearly") # long_term, yearly, quarterly, monthly, weekly, daily
    parent_goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True)
    target_date = Column(DateTime, nullable=True)
    progress = Column(Float, default=0.0) # 0-100
    status = Column(String(20), default="active") # active, completed, paused

    user = relationship("User", back_populates="goals")
    sub_goals = relationship("Goal", backref="parent_goal", remote_side=[id])

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), default="Study") # Study, Coding, Math, Health, Research
    frequency = Column(String(50), default="daily")
    target_days_per_week = Column(Integer, default=7)
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    color = Column(String(20), default="emerald")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    date = Column(String(10), nullable=False) # YYYY-MM-DD
    completed = Column(Boolean, default=True)
    value = Column(Float, default=1.0) # e.g. minutes or count

    habit = relationship("Habit", back_populates="logs")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    status = Column(String(30), default="in_progress") # planning, research, development, testing, deployed
    progress = Column(Float, default=0.0) # 0-100
    deadline = Column(DateTime, nullable=True)
    github_url = Column(String(500), default="")
    demo_url = Column(String(500), default="")
    technologies = Column(JSON, default=list) # ["PyTorch", "FastAPI", "React", "Docker"]
    cover_style = Column(String(50), default="gradient-neural")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="projects")
    tasks = relationship("ProjectTask", back_populates="project", cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="project", cascade="all, delete-orphan")

class ProjectTask(Base):
    __tablename__ = "project_tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="tasks")

class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    phase = Column(String(50), default="Development") # Planning, Research, Development, Testing, Deployment
    is_completed = Column(Boolean, default=False)
    target_date = Column(DateTime, nullable=True)
    order = Column(Integer, default=0)

    project = relationship("Project", back_populates="milestones")

class CodingProblem(Base):
    __tablename__ = "coding_problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    platform = Column(String(50), default="LeetCode") # LeetCode, Codeforces, HackerRank, GeeksforGeeks, Custom
    platform_problem_id = Column(String(50), default="")
    difficulty = Column(String(20), default="Medium") # Easy, Medium, Hard
    category = Column(String(100), default="Arrays & Hashing") # Dynamic Programming, Graphs, Trees, etc.
    tags = Column(JSON, default=list)
    url = Column(String(500), default="")
    solved = Column(Boolean, default=False)
    solve_time_minutes = Column(Integer, default=0)
    attempts = Column(Integer, default=1)
    notes = Column(Text, default="")
    last_attempted_at = Column(DateTime, nullable=True)

class CodingAttempt(Base):
    __tablename__ = "coding_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("coding_problems.id"), nullable=False)
    language = Column(String(50), default="Python")
    status = Column(String(30), default="Accepted") # Accepted, Wrong Answer, Time Limit Exceeded
    runtime_ms = Column(Integer, default=45)
    memory_mb = Column(Float, default=17.2)
    attempted_at = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(Text, default="")

    user = relationship("User", back_populates="coding_attempts")
    problem = relationship("CodingProblem")

class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50), default="")
    country = Column(String(100), nullable=False)
    city = Column(String(100), default="")
    ranking_world = Column(Integer, default=1)
    ranking_cs = Column(Integer, default=1)
    tuition_eur = Column(Float, default=0.0)
    semester_contribution_eur = Column(Float, default=0.0)
    website = Column(String(500), default="")
    logo_letter = Column(String(10), default="U")
    cover_image_key = Column(String(50), default="campus-classic")
    description = Column(Text, default="")

    programs = relationship("Program", back_populates="university", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="university")

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    name = Column(String(255), nullable=False) # e.g. M.Sc. Computer Science
    degree = Column(String(50), default="Master of Science")
    duration_semesters = Column(Integer, default=4)
    language = Column(String(50), default="English")
    application_deadline = Column(String(100), default="15 Dec / 15 Mar")
    gpa_requirement = Column(String(50), default="3.5 / 4.0 (German 1.8)")
    gre_requirement = Column(String(100), default="Required: V 155, Q 165, AW 4.0")
    language_requirement = Column(String(100), default="TOEFL 100+ or IELTS 7.5+")
    scholarship_opportunities = Column(String(255), default="ETH Excellence / DAAD / Merit")
    credits_ects = Column(Integer, default=120)

    university = relationship("University", back_populates="programs")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=True)
    status = Column(String(30), default="Researching") # Researching, Shortlisted, Preparing, Applied, Interview, Accepted, Rejected
    tier = Column(String(20), default="Target") # Dream, Target, Safe
    deadline = Column(DateTime, nullable=True)
    portal_url = Column(String(500), default="")
    application_fee_eur = Column(Float, default=100.0)
    notes = Column(Text, default="")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="applications")
    university = relationship("University", back_populates="applications")
    program = relationship("Program")
    documents = relationship("Document", back_populates="application", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    name = Column(String(255), nullable=False) # Statement of Purpose, LOR 1, LOR 2, Transcript, GRE, IELTS
    status = Column(String(30), default="Drafting") # Missing, Drafting, Review, Ready, Submitted
    file_path = Column(String(500), default="")
    notes = Column(Text, default="")

    application = relationship("Application", back_populates="documents")

class Deadline(Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(50), default="University") # University, Exam, Project, Goal
    due_date = Column(DateTime, nullable=False)
    is_completed = Column(Boolean, default=False)
    priority = Column(String(20), default="High")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, default="")
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="notes")
    topic = relationship("Topic", back_populates="notes")

class DailyPlan(Base):
    __tablename__ = "daily_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String(10), nullable=False) # YYYY-MM-DD
    available_hours = Column(Float, default=4.0)
    schedule_blocks = Column(JSON, default=list)
    daily_reflection_learned = Column(Text, default="")
    daily_reflection_difficulty = Column(Text, default="")
    daily_reflection_review = Column(Text, default="")
    daily_rating = Column(Integer, default=4) # 1 to 5 stars

    user = relationship("User", back_populates="daily_plans")

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), default="learning") # learning, coding, review, career
    title = Column(String(255), nullable=False)
    recommendation = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    action_label = Column(String(100), default="Start Learning")
    action_route = Column(String(255), default="/learn")
    priority_score = Column(Float, default=0.95)
    is_dismissed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(String(50), default="Milestone") # Streak, Mastery, Coding, Focus
    icon = Column(String(50), default="award")
    unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime, nullable=True)
    progress_current = Column(Integer, default=0)
    progress_max = Column(Integer, default=100)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String(50), default="reminder") # reminder, deadline, achievement, recommendation
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="notifications")
