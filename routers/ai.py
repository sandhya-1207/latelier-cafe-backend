import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Topic, Goal, CodingProblem, Application, User, DailyPlan
from schemas import AIPlannerRequest, AIPlannerResponse, AIChatRequest, AIChatResponse

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/planner", response_model=AIPlannerResponse)
def generate_ai_study_plan(request: AIPlannerRequest, db: Session = Depends(get_db)):
    hours = request.available_hours
    pref = request.focus_preference

    # Retrieve weakest topics and upcoming applications
    weak_topics = db.query(Topic).filter(Topic.mastery_percentage < 75.0).order_by(Topic.mastery_percentage.asc()).all()
    apps = db.query(Application).filter(Application.status.in_(["Preparing", "Shortlisted"])).all()

    # Time slot builder based on available hours
    total_minutes = int(hours * 60)
    current_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    
    schedule = []
    accumulated = 0

    # 1. Mathematics / Core Weakness Block (45-60 min)
    if accumulated + 45 <= total_minutes:
        m_topic = next((t for t in weak_topics if "Math" in t.subject.title or t.category == "Linear Algebra"), None)
        topic_name = m_topic.title if m_topic else "Eigenvalues & Spectral Theorem"
        start_str = current_time.strftime("%H:%M")
        current_time += datetime.timedelta(minutes=45)
        end_str = current_time.strftime("%H:%M")
        schedule.append({
            "time": f"{start_str} - {end_str}",
            "duration_minutes": 45,
            "subject": "Mathematics",
            "topic": topic_name,
            "type": "theory",
            "reason": "Spectral decomposition directly unlocks PCA and Graph Neural Network fundamentals.",
            "difficulty": "Hard"
        })
        accumulated += 45
        current_time += datetime.timedelta(minutes=10) # 10m break

    # 2. Python / Numerical Implementation Block (45 min)
    if accumulated + 45 <= total_minutes:
        start_str = current_time.strftime("%H:%M")
        current_time += datetime.timedelta(minutes=45)
        end_str = current_time.strftime("%H:%M")
        schedule.append({
            "time": f"{start_str} - {end_str}",
            "duration_minutes": 45,
            "subject": "Python",
            "topic": "NumPy Vectorized Strides & Einsum",
            "type": "practice",
            "reason": "Eliminates slow nested loops and builds speed required for custom autograd backprop.",
            "difficulty": "Medium"
        })
        accumulated += 45
        current_time += datetime.timedelta(minutes=10)

    # 3. Machine Learning / From-Scratch Model (50 min)
    if accumulated + 50 <= total_minutes:
        ml_topic = next((t for t in weak_topics if "Machine Learning" in t.subject.title), None)
        topic_name = ml_topic.title if ml_topic else "Linear & Ridge Regression Normal Equation"
        start_str = current_time.strftime("%H:%M")
        current_time += datetime.timedelta(minutes=50)
        end_str = current_time.strftime("%H:%M")
        schedule.append({
            "time": f"{start_str} - {end_str}",
            "duration_minutes": 50,
            "subject": "Machine Learning",
            "topic": topic_name,
            "type": "coding",
            "reason": "Direct algorithmic validation connecting matrix algebra to loss surface gradients.",
            "difficulty": "Medium"
        })
        accumulated += 50
        current_time += datetime.timedelta(minutes=10)

    # 4. Coding / LeetCode Problem Block (Remaining time, e.g. 30-60 min)
    if accumulated + 30 <= total_minutes:
        dur = min(60, total_minutes - accumulated)
        start_str = current_time.strftime("%H:%M")
        current_time += datetime.timedelta(minutes=dur)
        end_str = current_time.strftime("%H:%M")
        schedule.append({
            "time": f"{start_str} - {end_str}",
            "duration_minutes": dur,
            "subject": "Coding",
            "topic": "Graph Topological Sort & Cycle Detection",
            "type": "practice",
            "reason": "Reinforces DAG dependency resolution essential for technical interviews and ML pipelines.",
            "difficulty": "Hard"
        })
        accumulated += dur

    # Save to today's daily plan
    user = db.query(User).first()
    today_str = str(datetime.date.today())
    dp = db.query(DailyPlan).filter(DailyPlan.date == today_str).first()
    if dp:
        dp.available_hours = hours
        dp.schedule_blocks = schedule
        db.commit()

    insights = f"Generated optimal {hours}h schedule balancing foundational mathematical rigor with hands-on coding. We prioritized high-impact dependency bottlenecks."
    return {
        "date": today_str,
        "available_hours": hours,
        "schedule": schedule,
        "insights": insights
    }

@router.post("/chat", response_model=AIChatResponse)
def ai_assistant_chat(req: AIChatRequest, db: Session = Depends(get_db)):
    msg = req.message.lower().strip()

    if "study today" in msg or "what should i study" in msg:
        reply = (
            "### Recommended Study Priority for Today\n\n"
            "Based on your current curriculum dependencies and upcoming Master's applications:\n\n"
            "1. **Mathematics (45m)**: *Eigenvalues & Spectral Theorem*\n"
            "   - **Why**: Your linear algebra mastery is at 68%. This is the primary blocker for PCA and Singular Value Decomposition.\n\n"
            "2. **Machine Learning (50m)**: *Linear & Ridge Regression from Scratch*\n"
            "   - **Why**: Verify your normal equations and compare analytical inversion against gradient descent.\n\n"
            "3. **Coding (45m)**: *Alien Dictionary / Course Schedule II*\n"
            "   - **Why**: Solidify Topological Sort on DAGs.\n\n"
            "Would you like me to push this schedule directly into your **Today Command Center**?"
        )
        actions = [
            {"label": "Apply Schedule to Today", "route": "/today"},
            {"label": "Start 45m Pomodoro", "route": "/focus"}
        ]
    elif "calculus" in msg or "weak in calculus" in msg:
        reply = (
            "### Calculus & Optimization Analysis\n\n"
            "Your Multivariable Calculus progress sits at **82%**, with specific friction around **Hessian matrix curvature** and second-order Taylor approximations.\n\n"
            "**Key Insights:**\n"
            "- You understand gradient vectors $\\nabla f(x)$ well in 2D and 3D.\n"
            "- The bottleneck occurs when mapping multi-dimensional Jacobians into tensor contractions in neural network backpropagation.\n\n"
            "**Recommended Action:**\n"
            "Work through the 3 practice derivations on vector-by-matrix Jacobians before implementing custom PyTorch autograd functions."
        )
        actions = [
            {"label": "Open Calculus Topics", "route": "/topic/6"},
            {"label": "Launch Skill Graph", "route": "/skills"}
        ]
    elif "neural network" in msg or "before neural network" in msg:
        reply = (
            "### Prerequisites for Deep Learning & Neural Networks\n\n"
            "Before diving deep into transformer attention and backpropagation, ensure you have these foundations locked in:\n\n"
            "1. **Multivariable Calculus**: Partial derivatives and the multivariate chain rule $\\frac{\\partial L}{\\partial W} = \\frac{\\partial L}{\\partial y} \\cdot \\frac{\\partial y}{\\partial W}$.\n"
            "2. **Linear Algebra**: Matrix multiplications, vector projections, and transpose properties $(AB)^T = B^T A^T$.\n"
            "3. **NumPy Vectorization**: Broadcasting rules across batch dimensions without explicit Python loops.\n\n"
            "You have already mastered 2 of these 3! You are in an excellent position to progress."
        )
        actions = [
            {"label": "View Neural Networks Topic", "route": "/topic/10"},
            {"label": "Inspect Knowledge Graph", "route": "/skills"}
        ]
    elif "plan" in msg or "2-week" in msg:
        reply = (
            "### 2-Week Accelerated ML Engineering Sprint\n\n"
            "- **Week 1 (Foundations & Autograd)**:\n"
            "  - Days 1–3: Implement scalar and 2D Tensor autograd with reverse-mode automatic differentiation.\n"
            "  - Days 4–5: Numerical gradient verification with finite differences.\n"
            "  - Days 6–7: Multi-Layer Perceptron trained on non-linear spiral datasets.\n\n"
            "- **Week 2 (Transformers & Master's Dossier)**:\n"
            "  - Days 8–10: Scaled dot-product multi-head self-attention module in NumPy.\n"
            "  - Days 11–12: Vision Transformer patch projection and position embeddings.\n"
            "  - Days 13–14: Complete ETH Zurich Statement of Purpose draft and push GitHub release."
        )
        actions = [
            {"label": "View Projects Tracker", "route": "/projects"},
            {"label": "Open Master's Pipeline", "route": "/masters"}
        ]
    else:
        reply = (
            f"### Academic Advisor Analysis\n\n"
            f"I analyzed your request regarding: *\"{req.message}\"*\n\n"
            "Looking across your 216.5 verified study hours, 14-day streak, and 88.5% coding accuracy:\n"
            "- **Current High-Leverage Focus**: Finalize the Vision Transformer project milestones and keep your daily coding streak consistent.\n"
            "- **Master's Preparation**: Ensure your second Recommendation Letter is submitted for ETH Zurich within the next 2 weeks.\n\n"
            "Feel free to ask for a custom daily schedule, prerequisite diagnosis, or code derivation breakdown."
        )
        actions = [
            {"label": "Generate AI Daily Plan", "route": "/ai/planner"},
            {"label": "View Knowledge Graph", "route": "/skills"}
        ]

    return {"reply": reply, "suggested_actions": actions}
