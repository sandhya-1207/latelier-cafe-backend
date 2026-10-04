import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
from database import SessionLocal, engine, Base
from models import (
    User, Profile, Subject, Topic, Subtopic, Skill, SkillDependency,
    Task, StudySession, Goal, Habit, HabitLog, Project, ProjectTask,
    Milestone, CodingProblem, CodingAttempt, University, Program,
    Application, Document, Deadline, Note, DailyPlan, AIRecommendation,
    Achievement, Notification
)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if already seeded
    if db.query(User).first():
        db.close()
        return

    print("Seeding StudyOS database with realistic sample data...")

    # 1. User & Profile
    user = User(
        email="alex.mercer@studyos.ai",
        hashed_password="demo_password_hash",
        name="Alex Mercer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    profile = Profile(
        user_id=user.id,
        academic_year="Senior / Final Year Undergrad",
        target_degree="M.Sc. Computer Science & Artificial Intelligence",
        career_goal="Machine Learning Research Engineer / AI Scientist",
        target_countries=["Switzerland", "Germany", "United States", "United Kingdom"],
        daily_study_goal_hours=4.5,
        current_streak=14,
        longest_streak=28,
        total_study_hours=216.5,
        avatar_url="",
        theme="dark"
    )
    db.add(profile)

    # 2. Subjects
    sub_python = Subject(
        slug="python",
        title="Python Mastery",
        description="Core language, advanced metaprogramming, vectorization, and high-performance computing.",
        icon="terminal",
        color="emerald",
        order=1
    )
    sub_math = Subject(
        slug="mathematics",
        title="Mathematics for Machine Learning",
        description="Rigorous Linear Algebra, Multivariable Calculus, Probability, and Numerical Optimization.",
        icon="sigma",
        color="indigo",
        order=2
    )
    sub_ml = Subject(
        slug="machine-learning",
        title="Machine Learning & Deep Learning",
        description="Statistical learning theory, classical algorithms, neural architectures, and implementations from scratch.",
        icon="brain",
        color="violet",
        order=3
    )
    sub_cs = Subject(
        slug="computer-science",
        title="Computer Science & Algorithms",
        description="Data structures, dynamic programming, graph algorithms, asymptotic analysis, and systems.",
        icon="cpu",
        color="amber",
        order=4
    )
    db.add_all([sub_python, sub_math, sub_ml, sub_cs])
    db.commit()
    db.refresh(sub_python)
    db.refresh(sub_math)
    db.refresh(sub_ml)
    db.refresh(sub_cs)

    # 3. Topics
    # Python Topics
    t_py_basics = Topic(
        subject_id=sub_python.id,
        title="Python Data Models & Idioms",
        slug="python-data-models",
        description="Dunder methods, memory model, iterables protocol, and collections framework.",
        category="Foundations",
        difficulty="Beginner",
        status="mastered",
        mastery_percentage=95.0,
        theory_mastery=98.0,
        math_mastery=80.0,
        impl_mastery=96.0,
        time_spent_minutes=720,
        problems_solved=14,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=4),
        order=1,
        prerequisites=[],
        related_topics=["Object-Oriented Architecture", "Generators & Itertools"],
        ml_applications=["Custom Dataset Loaders", "PyTorch Module Subclassing"]
    )
    t_py_numpy = Topic(
        subject_id=sub_python.id,
        title="NumPy Vectorization & Memory Strides",
        slug="numpy-vectorization",
        description="Strided arrays, broadcasting rules, C-contiguous memory layouts, and BLAS operations.",
        category="Numerical Computing",
        difficulty="Intermediate",
        status="in_progress",
        mastery_percentage=85.0,
        theory_mastery=90.0,
        math_mastery=85.0,
        impl_mastery=82.0,
        time_spent_minutes=940,
        problems_solved=22,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        order=2,
        prerequisites=["Python Data Models & Idioms"],
        related_topics=["Eigenvalues & Eigenvectors", "Linear Regression from Scratch"],
        ml_applications=["Matrix Operations in Deep Learning", "Custom Loss Functions"]
    )
    t_py_perf = Topic(
        subject_id=sub_python.id,
        title="High Performance Python & Concurrency",
        slug="high-performance-python",
        description="GIL internals, asyncio event loops, multiprocessing, Numba JIT, and Cython.",
        category="Advanced Systems",
        difficulty="Advanced",
        status="review",
        mastery_percentage=55.0,
        theory_mastery=65.0,
        math_mastery=40.0,
        impl_mastery=52.0,
        time_spent_minutes=480,
        problems_solved=6,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=6),
        order=3,
        prerequisites=["NumPy Vectorization & Memory Strides"],
        related_topics=["Algorithmic Complexity", "Parallel DataLoader pipelines"],
        ml_applications=["Distributed Training Bottleneck Profiling"]
    )

    # Mathematics Topics
    t_math_eigen = Topic(
        subject_id=sub_math.id,
        title="Eigenvalues, Eigenvectors & Spectral Theorem",
        slug="eigenvalues-eigenvectors",
        description="Characteristic polynomials, diagonalizability, symmetric matrices, and geometric interpretations of linear transformations.",
        category="Linear Algebra",
        difficulty="Intermediate",
        status="in_progress",
        mastery_percentage=68.0,
        theory_mastery=75.0,
        math_mastery=70.0,
        impl_mastery=60.0,
        time_spent_minutes=860,
        problems_solved=16,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(hours=8),
        order=1,
        prerequisites=["Vector Spaces & Matrix Rank", "Determinants & Invertibility"],
        related_topics=["Singular Value Decomposition (SVD)", "Principal Component Analysis (PCA)"],
        ml_applications=["Dimensionality Reduction", "Graph Convolutional Networks (Laplacian spectrum)", "PageRank"]
    )
    t_math_svd = Topic(
        subject_id=sub_math.id,
        title="Singular Value Decomposition (SVD) & Pseudoinverse",
        slug="svd-pseudoinverse",
        description="Four fundamental subspaces, low-rank matrix approximation, Moore-Penrose pseudoinverse, and condition numbers.",
        category="Linear Algebra",
        difficulty="Advanced",
        status="in_progress",
        mastery_percentage=62.0,
        theory_mastery=70.0,
        math_mastery=65.0,
        impl_mastery=50.0,
        time_spent_minutes=610,
        problems_solved=9,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=2),
        order=2,
        prerequisites=["Eigenvalues, Eigenvectors & Spectral Theorem"],
        related_topics=["Principal Component Analysis (PCA)", "Latent Semantic Analysis"],
        ml_applications=["Recommendation Systems (Matrix Factorization)", "Image Compression", "Weight Initialization"]
    )
    t_math_calc = Topic(
        subject_id=sub_math.id,
        title="Multivariable Calculus, Jacobians & Hessians",
        slug="multivariable-calculus-gradients",
        description="Vector-valued calculus, directional derivatives, Jacobian matrices, Hessian curvature, and Taylor approximations.",
        category="Calculus & Optimization",
        difficulty="Intermediate",
        status="in_progress",
        mastery_percentage=82.0,
        theory_mastery=88.0,
        math_mastery=84.0,
        impl_mastery=74.0,
        time_spent_minutes=910,
        problems_solved=19,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        order=3,
        prerequisites=["Single Variable Calculus"],
        related_topics=["Convex Optimization & Gradient Descent", "Backpropagation Calculus"],
        ml_applications=["Automatic Differentiation Engines", "Second-Order Optimizers (L-BFGS)", "Loss Surface Curvature"]
    )
    t_math_prob = Topic(
        subject_id=sub_math.id,
        title="Probability Distributions & Bayesian Inference",
        slug="probability-bayesian-inference",
        description="Random variables, Multivariate Normal distribution, maximum likelihood estimation (MLE), and Maximum A Posteriori (MAP).",
        category="Probability & Statistics",
        difficulty="Intermediate",
        status="mastered",
        mastery_percentage=90.0,
        theory_mastery=92.0,
        math_mastery=90.0,
        impl_mastery=88.0,
        time_spent_minutes=1100,
        problems_solved=24,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=3),
        order=4,
        prerequisites=["Calculus & Integration"],
        related_topics=["Gaussian Processes", "Variational Autoencoders"],
        ml_applications=["Bayesian Neural Networks", "Information Criterion (AIC/BIC)", "Naive Bayes"]
    )

    # Machine Learning Topics
    t_ml_reg = Topic(
        subject_id=sub_ml.id,
        title="Linear & Logistic Regression from Scratch",
        slug="regression-from-scratch",
        description="Derivation of normal equations, gradient descent dynamics, L1/L2 Lasso/Ridge regularization, and ROC-AUC metrics.",
        category="Supervised Learning",
        difficulty="Beginner",
        status="mastered",
        mastery_percentage=94.0,
        theory_mastery=96.0,
        math_mastery=95.0,
        impl_mastery=92.0,
        time_spent_minutes=1250,
        problems_solved=18,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=2),
        order=1,
        prerequisites=["NumPy Vectorization & Memory Strides", "Multivariable Calculus, Jacobians & Hessians"],
        related_topics=["Convex Optimization & Gradient Descent", "Support Vector Machines"],
        ml_applications=["Baseline Modeling", "Risk Scoring", "Explainable AI"]
    )
    t_ml_pca = Topic(
        subject_id=sub_ml.id,
        title="Principal Component Analysis & Manifold Learning",
        slug="pca-manifold-learning",
        description="Covariance matrix formulation, projection onto principal components, t-SNE, and UMAP non-linear embeddings.",
        category="Unsupervised Learning",
        difficulty="Intermediate",
        status="in_progress",
        mastery_percentage=72.0,
        theory_mastery=78.0,
        math_mastery=75.0,
        impl_mastery=64.0,
        time_spent_minutes=780,
        problems_solved=11,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=3),
        order=2,
        prerequisites=["Eigenvalues, Eigenvectors & Spectral Theorem", "Singular Value Decomposition (SVD) & Pseudoinverse"],
        related_topics=["Unsupervised Representation Learning", "Autoencoders"],
        ml_applications=["High-Dimensional Feature Compression", "Bioinformatics Gene Expression", "Data Visualization"]
    )
    t_ml_nn = Topic(
        subject_id=sub_ml.id,
        title="Multi-Layer Perceptrons & Computational Graphs",
        slug="mlp-computational-graphs",
        description="Reverse-mode automatic differentiation, chain rule tensor contractions, activation functions (GELU/Swish), and initialization schemes (He/Xavier).",
        category="Deep Learning",
        difficulty="Intermediate",
        status="in_progress",
        mastery_percentage=78.0,
        theory_mastery=82.0,
        math_mastery=80.0,
        impl_mastery=72.0,
        time_spent_minutes=1340,
        problems_solved=15,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(hours=14),
        order=3,
        prerequisites=["Multivariable Calculus, Jacobians & Hessians", "Linear & Logistic Regression from Scratch"],
        related_topics=["Convolutional Neural Networks", "Transformers & Attention Mechanisms"],
        ml_applications=["Deep Representation Learning", "Foundation Models Backbone"]
    )
    t_ml_transformers = Topic(
        subject_id=sub_ml.id,
        title="Transformers & Scaled Dot-Product Attention",
        slug="transformers-self-attention",
        description="Query-Key-Value attention mechanics, multi-head attention, rotary positional embeddings (RoPE), LayerNorm vs RMSNorm, and KV caching.",
        category="Deep Learning",
        difficulty="Advanced",
        status="in_progress",
        mastery_percentage=52.0,
        theory_mastery=65.0,
        math_mastery=58.0,
        impl_mastery=40.0,
        time_spent_minutes=820,
        problems_solved=7,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        order=4,
        prerequisites=["Multi-Layer Perceptrons & Computational Graphs"],
        related_topics=["Vision Transformers", "Large Language Models"],
        ml_applications=["Modern LLMs (LLaMA, GPT)", "Speech Recognition (Whisper)", "Protein Folding (AlphaFold)"]
    )

    # CS & Algorithms Topics
    t_cs_graphs = Topic(
        subject_id=sub_cs.id,
        title="Graph Algorithms & Network Traversal",
        slug="graph-algorithms-traversal",
        description="Breadth-First Search, Depth-First Search, Topological Sorting (Kahn's & DFS), Shortest Paths (Dijkstra, Bellman-Ford), and Disjoint Set Union.",
        category="Data Structures & Algorithms",
        difficulty="Intermediate",
        status="in_progress",
        mastery_percentage=84.0,
        theory_mastery=90.0,
        math_mastery=80.0,
        impl_mastery=82.0,
        time_spent_minutes=1420,
        problems_solved=32,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        order=1,
        prerequisites=["Basic Trees & Queues"],
        related_topics=["Dynamic Programming on Trees", "Graph Neural Networks"],
        ml_applications=["Computational Graphs Scheduling", "Knowledge Graphs", "Dependency Resolution"]
    )
    t_cs_dp = Topic(
        subject_id=sub_cs.id,
        title="Dynamic Programming & Memoization Strategies",
        slug="dynamic-programming-patterns",
        description="Optimal substructure, overlapping subproblems, 0/1 Knapsack variations, Longest Common Subsequence, and state-compression DP with bitmasks.",
        category="Data Structures & Algorithms",
        difficulty="Advanced",
        status="in_progress",
        mastery_percentage=66.0,
        theory_mastery=78.0,
        math_mastery=72.0,
        impl_mastery=58.0,
        time_spent_minutes=1680,
        problems_solved=38,
        last_studied_at=datetime.datetime.utcnow() - datetime.timedelta(days=2),
        order=2,
        prerequisites=["Recursion & Backtracking"],
        related_topics=["Markov Decision Processes", "Reinforcement Learning Value Iteration"],
        ml_applications=["Viterbi Algorithm (HMMs)", "Beam Search Decoding in NLP"]
    )

    db.add_all([
        t_py_basics, t_py_numpy, t_py_perf,
        t_math_eigen, t_math_svd, t_math_calc, t_math_prob,
        t_ml_reg, t_ml_pca, t_ml_nn, t_ml_transformers,
        t_cs_graphs, t_cs_dp
    ])
    db.commit()

    # Subtopics for Eigenvalues
    db.add_all([
        Subtopic(topic_id=t_math_eigen.id, title="Geometric intuition of Ax = λx", is_completed=True, understanding_score=4.8),
        Subtopic(topic_id=t_math_eigen.id, title="Computing det(A - λI) = 0 and algebraic multiplicity", is_completed=True, understanding_score=4.5),
        Subtopic(topic_id=t_math_eigen.id, title="Eigenspaces and geometric multiplicity", is_completed=True, understanding_score=4.2),
        Subtopic(topic_id=t_math_eigen.id, title="Spectral Theorem for real symmetric matrices", is_completed=False, understanding_score=3.0),
        Subtopic(topic_id=t_math_eigen.id, title="Rayleigh quotient and Principal Axis theorem", is_completed=False, understanding_score=2.5),
    ])

    # Subtopics for NumPy
    db.add_all([
        Subtopic(topic_id=t_py_numpy.id, title="Memory buffer layouts and strides (C vs Fortran order)", is_completed=True, understanding_score=4.7),
        Subtopic(topic_id=t_py_numpy.id, title="Broadcasting rules and zero-copy view semantics", is_completed=True, understanding_score=4.9),
        Subtopic(topic_id=t_py_numpy.id, title="Einsum notation for multi-dimensional tensor contractions", is_completed=True, understanding_score=4.0),
        Subtopic(topic_id=t_py_numpy.id, title="Vectorized pairwise distance matrix calculation without loops", is_completed=False, understanding_score=3.5),
    ])
    db.commit()

    # 4. Interactive Knowledge Graph Skills & Dependencies
    skills = [
        Skill(name="Python Foundations", category="python", level="Advanced", proficiency=95.0, importance=5),
        Skill(name="NumPy & Vectorization", category="python", level="Intermediate", proficiency=85.0, importance=5),
        Skill(name="PyTorch Internal Architecture", category="python", level="Intermediate", proficiency=75.0, importance=5),
        Skill(name="Linear Algebra Basics", category="math", level="Advanced", proficiency=90.0, importance=5),
        Skill(name="Eigenvalues & Eigenvectors", category="math", level="Intermediate", proficiency=68.0, importance=5),
        Skill(name="Singular Value Decomposition", category="math", level="Intermediate", proficiency=62.0, importance=4),
        Skill(name="Multivariable Calculus & Gradients", category="math", level="Advanced", proficiency=82.0, importance=5),
        Skill(name="Probability & Statistics", category="math", level="Advanced", proficiency=90.0, importance=4),
        Skill(name="Linear Regression", category="ml", level="Advanced", proficiency=94.0, importance=4),
        Skill(name="PCA & Dimensionality Reduction", category="ml", level="Intermediate", proficiency=72.0, importance=4),
        Skill(name="Neural Networks & Backprop", category="ml", level="Intermediate", proficiency=78.0, importance=5),
        Skill(name="Attention & Transformers", category="ml", level="Intermediate", proficiency=52.0, importance=5),
        Skill(name="Graph Algorithms", category="cs", level="Advanced", proficiency=84.0, importance=4),
        Skill(name="Dynamic Programming", category="cs", level="Intermediate", proficiency=66.0, importance=5),
    ]
    db.add_all(skills)

    deps = [
        SkillDependency(source_skill="Python Foundations", target_skill="NumPy & Vectorization", relationship_type="foundation"),
        SkillDependency(source_skill="NumPy & Vectorization", target_skill="Linear Regression", relationship_type="prerequisite"),
        SkillDependency(source_skill="NumPy & Vectorization", target_skill="PyTorch Internal Architecture", relationship_type="prerequisite"),
        SkillDependency(source_skill="Linear Algebra Basics", target_skill="Eigenvalues & Eigenvectors", relationship_type="prerequisite"),
        SkillDependency(source_skill="Eigenvalues & Eigenvectors", target_skill="Singular Value Decomposition", relationship_type="prerequisite"),
        SkillDependency(source_skill="Eigenvalues & Eigenvectors", target_skill="PCA & Dimensionality Reduction", relationship_type="prerequisite"),
        SkillDependency(source_skill="Multivariable Calculus & Gradients", target_skill="Neural Networks & Backprop", relationship_type="prerequisite"),
        SkillDependency(source_skill="Neural Networks & Backprop", target_skill="Attention & Transformers", relationship_type="prerequisite"),
        SkillDependency(source_skill="PyTorch Internal Architecture", target_skill="Attention & Transformers", relationship_type="co_requisite"),
        SkillDependency(source_skill="Graph Algorithms", target_skill="Neural Networks & Backprop", relationship_type="foundation"),
    ]
    db.add_all(deps)
    db.commit()

    # 5. Today's Tasks
    tasks = [
        Task(
            user_id=user.id,
            title="Linear Algebra: Spectral Theorem proof & Rayleigh quotient",
            subject="Mathematics",
            topic_id=t_math_eigen.id,
            estimated_duration_minutes=45,
            difficulty="Hard",
            priority="High",
            status="pending",
            is_today=True,
            progress_percentage=20,
            due_date=datetime.datetime.utcnow().replace(hour=18, minute=0)
        ),
        Task(
            user_id=user.id,
            title="NumPy: Vectorized batch Mahalanobis distance without Python loops",
            subject="Python",
            topic_id=t_py_numpy.id,
            estimated_duration_minutes=40,
            difficulty="Medium",
            priority="Medium",
            status="in_progress",
            is_today=True,
            progress_percentage=60,
            due_date=datetime.datetime.utcnow().replace(hour=19, minute=30)
        ),
        Task(
            user_id=user.id,
            title="Machine Learning: Implement Ridge regression closed-form vs SGD solver",
            subject="Machine Learning",
            topic_id=t_ml_reg.id,
            estimated_duration_minutes=50,
            difficulty="Medium",
            priority="High",
            status="pending",
            is_today=True,
            progress_percentage=0,
            due_date=datetime.datetime.utcnow().replace(hour=21, minute=0)
        ),
        Task(
            user_id=user.id,
            title="Coding: Solve 3 LeetCode Graph problems (Topological sort & Kahn's algorithm)",
            subject="Coding",
            topic_id=t_cs_graphs.id,
            estimated_duration_minutes=60,
            difficulty="Hard",
            priority="High",
            status="completed",
            is_today=True,
            progress_percentage=100,
            completed_at=datetime.datetime.utcnow() - datetime.timedelta(hours=2)
        ),
        Task(
            user_id=user.id,
            title="Master's Prep: Finalize statement of purpose for ETH Zurich AI program",
            subject="Master's Preparation",
            estimated_duration_minutes=45,
            difficulty="Medium",
            priority="Urgent",
            status="pending",
            is_today=True,
            progress_percentage=50,
            due_date=datetime.datetime.utcnow().replace(hour=22, minute=30)
        ),
    ]
    db.add_all(tasks)

    # 6. Coding Problems
    coding_problems = [
        CodingProblem(
            title="Course Schedule II (Topological Sort / Kahn's)",
            platform="LeetCode",
            platform_problem_id="210",
            difficulty="Medium",
            category="Graphs",
            tags=["Graph", "Topological Sort", "BFS", "DFS"],
            url="https://leetcode.com/problems/course-schedule-ii/",
            solved=True,
            solve_time_minutes=24,
            attempts=1,
            notes="Implemented using in-degree array and queue (Kahn's algorithm). O(V + E) time, O(V + E) space. Crucial for understanding task dependencies."
        ),
        CodingProblem(
            title="Trapping Rain Water (Two Pointers & Monotonic Stack)",
            platform="LeetCode",
            platform_problem_id="42",
            difficulty="Hard",
            category="Two Pointers",
            tags=["Array", "Two Pointers", "Dynamic Programming", "Stack"],
            url="https://leetcode.com/problems/trapping-rain-water/",
            solved=True,
            solve_time_minutes=35,
            attempts=2,
            notes="Two-pointer approach maintaining max_left and max_right keeps space complexity at O(1)."
        ),
        CodingProblem(
            title="Coin Change (1D Dynamic Programming)",
            platform="LeetCode",
            platform_problem_id="322",
            difficulty="Medium",
            category="Dynamic Programming",
            tags=["Array", "Dynamic Programming", "BFS"],
            url="https://leetcode.com/problems/coin-change/",
            solved=True,
            solve_time_minutes=18,
            attempts=1,
            notes="Bottom-up DP: dp[i] = min(dp[i], dp[i - c] + 1). Initialized with float('inf')."
        ),
        CodingProblem(
            title="LRU Cache (Hash Map + Doubly Linked List)",
            platform="LeetCode",
            platform_problem_id="146",
            difficulty="Medium",
            category="Design & Linked List",
            tags=["Hash Table", "Linked List", "Design", "Doubly-Linked List"],
            url="https://leetcode.com/problems/lru-cache/",
            solved=True,
            solve_time_minutes=28,
            attempts=1,
            notes="Used dummy head and tail nodes to avoid edge cases during node removal and insertion."
        ),
        CodingProblem(
            title="Word Break (Trie + 1D DP)",
            platform="LeetCode",
            platform_problem_id="139",
            difficulty="Medium",
            category="Dynamic Programming",
            tags=["Array", "Hash Table", "String", "Dynamic Programming", "Trie"],
            url="https://leetcode.com/problems/word-break/",
            solved=False,
            solve_time_minutes=0,
            attempts=1,
            notes="Need to review state transition: dp[i] = any(dp[j] and s[j:i] in wordSet for j in range(i))."
        ),
        CodingProblem(
            title="Alien Dictionary (Directed Acyclic Graph & Topological Sort)",
            platform="LeetCode",
            platform_problem_id="269",
            difficulty="Hard",
            category="Graphs",
            tags=["Array", "String", "Graph", "Topological Sort"],
            url="https://leetcode.com/problems/alien-dictionary/",
            solved=False,
            solve_time_minutes=0,
            attempts=0,
            notes="Key edge case: word prefixes appearing in wrong order (e.g. ['abc', 'ab']) invalidates graph immediately."
        ),
        CodingProblem(
            title="Longest Increasing Subsequence (Patience Sorting O(N log N))",
            platform="LeetCode",
            platform_problem_id="300",
            difficulty="Medium",
            category="Binary Search & DP",
            tags=["Array", "Binary Search", "Dynamic Programming"],
            url="https://leetcode.com/problems/longest-increasing-subsequence/",
            solved=True,
            solve_time_minutes=22,
            attempts=1,
            notes="Classic patience sorting algorithm using bisect_left."
        ),
        CodingProblem(
            title="Network Delay Time (Dijkstra's Shortest Path)",
            platform="LeetCode",
            platform_problem_id="743",
            difficulty="Medium",
            category="Graphs",
            tags=["Depth-First Search", "Breadth-First Search", "Graph", "Heap (Priority Queue)", "Shortest Path"],
            url="https://leetcode.com/problems/network-delay-time/",
            solved=True,
            solve_time_minutes=25,
            attempts=1,
            notes="Min-heap with (dist, node). If max(dist) is inf, return -1."
        ),
    ]
    db.add_all(coding_problems)

    # 7. Projects
    p1 = Project(
        user_id=user.id,
        title="Micro-Autograd & Vision Transformer from Scratch",
        description="A lightweight pure Python and NumPy implementation of an autograd engine with reverse-mode computational graph construction, followed by a modular Vision Transformer (ViT) implementation trained on CIFAR-10.",
        status="development",
        progress=68.0,
        deadline=datetime.datetime.utcnow() + datetime.timedelta(days=28),
        github_url="https://github.com/alexmercer/micro-autograd-vit",
        demo_url="https://vit-demo.studyos.ai",
        technologies=["Python", "NumPy", "PyTorch (benchmarking)", "Docker", "Weights & Biases"],
        cover_style="neural-mesh"
    )
    p2 = Project(
        user_id=user.id,
        title="High-Frequency Quantitative Backtester Engine",
        description="Event-driven algorithmic trading and order execution simulator supporting tick-level limit order books, slippage modeling, and vectorized performance analytics.",
        status="research",
        progress=35.0,
        deadline=datetime.datetime.utcnow() + datetime.timedelta(days=60),
        github_url="https://github.com/alexmercer/quant-backtester-core",
        demo_url="",
        technologies=["Python", "Pandas", "FastAPI", "Polars", "C++ (bindings)"],
        cover_style="geometric-grid"
    )
    p3 = Project(
        user_id=user.id,
        title="Spectral Graph Clustering & Community Detection",
        description="Implementing normalized graph Laplacians, Cheeger inequalities, and spectral decomposition algorithms applied to large-scale social networks and citation graphs.",
        status="testing",
        progress=90.0,
        deadline=datetime.datetime.utcnow() + datetime.timedelta(days=7),
        github_url="https://github.com/alexmercer/spectral-graph-suite",
        demo_url="https://spectral.studyos.ai",
        technologies=["Python", "SciPy", "NetworkX", "Matplotlib", "FastAPI"],
        cover_style="spectral-graph"
    )
    db.add_all([p1, p2, p3])
    db.commit()
    db.refresh(p1)

    # Milestones for Project 1
    db.add_all([
        Milestone(project_id=p1.id, title="1. Scalar Value Class & Backward Propagation Chain Rule", phase="Planning", is_completed=True, order=1),
        Milestone(project_id=p1.id, title="2. Tensor Tensor-Operations & Broadcast Gradient Routing", phase="Research", is_completed=True, order=2),
        Milestone(project_id=p1.id, title="3. Scaled Dot-Product Attention & Multi-Head Block in pure NumPy", phase="Development", is_completed=True, order=3),
        Milestone(project_id=p1.id, title="4. Patch Extraction Layer & Positional Embedding Verification", phase="Development", is_completed=False, order=4),
        Milestone(project_id=p1.id, title="5. CIFAR-10 Convergence Training & PyTorch Parity Tests", phase="Testing", is_completed=False, order=5),
        Milestone(project_id=p1.id, title="6. Interactive Inference Demo & Research Paper Writeup", phase="Deployment", is_completed=False, order=6),
    ])

    db.add_all([
        ProjectTask(project_id=p1.id, title="Write unit tests for tensor transpositions in 4D attention batching", completed=True),
        ProjectTask(project_id=p1.id, title="Debug numerical gradient checking with finite differences epsilon=1e-5", completed=True),
        ProjectTask(project_id=p1.id, title="Implement patch tokenizer (16x16 flattened projection)", completed=False),
        ProjectTask(project_id=p1.id, title="Benchmark execution speed vs native PyTorch backward pass", completed=False),
    ])

    # 8. Universities & Master's Tracker
    uni_eth = University(
        name="ETH Zurich (Swiss Federal Institute of Technology)",
        short_name="ETH Zurich",
        country="Switzerland",
        city="Zurich",
        ranking_world=7,
        ranking_cs=9,
        tuition_eur=1500.0,
        semester_contribution_eur=750.0,
        website="https://ethz.ch/en.html",
        logo_letter="ETH",
        cover_image_key="eth-zurich",
        description="World-renowned engineering powerhouse. The Department of Computer Science has world-class faculty in Machine Learning, Robotics, and Computer Vision."
    )
    uni_tum = University(
        name="Technical University of Munich",
        short_name="TUM",
        country="Germany",
        city="Munich",
        ranking_world=28,
        ranking_cs=18,
        tuition_eur=6000.0,
        semester_contribution_eur=152.0,
        website="https://www.tum.de/en/",
        logo_letter="TUM",
        cover_image_key="tum-munich",
        description="Top European university with strong industry ties to BMW, Siemens, and leading AI labs in Munich. Elite Master in Informatics and Data Engineering."
    )
    uni_cmu = University(
        name="Carnegie Mellon University",
        short_name="CMU",
        country="United States",
        city="Pittsburgh, PA",
        ranking_world=24,
        ranking_cs=1,
        tuition_eur=56000.0,
        semester_contribution_eur=1200.0,
        website="https://www.cmu.edu/",
        logo_letter="CMU",
        cover_image_key="cmu-pittsburgh",
        description="The quintessential epicenter of Computer Science and Machine Learning. School of Computer Science (SCS) and Machine Learning Department (MLD)."
    )
    uni_stanford = University(
        name="Stanford University",
        short_name="Stanford",
        country="United States",
        city="Stanford, CA",
        ranking_world=3,
        ranking_cs=2,
        tuition_eur=62000.0,
        semester_contribution_eur=1400.0,
        website="https://www.stanford.edu/",
        logo_letter="STAN",
        cover_image_key="stanford-california",
        description="Silicon Valley epicenter. Leading research in Foundation Models, Artificial Intelligence, Robotics, and Systems."
    )
    uni_oxford = University(
        name="University of Oxford",
        short_name="Oxford",
        country="United Kingdom",
        city="Oxford",
        ranking_world=1,
        ranking_cs=4,
        tuition_eur=38000.0,
        semester_contribution_eur=800.0,
        website="https://www.ox.ac.uk/",
        logo_letter="OXF",
        cover_image_key="oxford-uk",
        description="Historical academic prestige combined with pioneering AI research through the Oxford Machine Learning Research Group and Oxford Robotics Institute."
    )
    uni_epfl = University(
        name="École Polytechnique Fédérale de Lausanne",
        short_name="EPFL",
        country="Switzerland",
        city="Lausanne",
        ranking_world=16,
        ranking_cs=12,
        tuition_eur=1500.0,
        semester_contribution_eur=780.0,
        website="https://www.epfl.ch/en/",
        logo_letter="EPFL",
        cover_image_key="epfl-lausanne",
        description="Sister school to ETH Zurich located on Lake Geneva. World-class in Data Science, Computational Neuroscience, and Machine Learning systems."
    )
    db.add_all([uni_eth, uni_tum, uni_cmu, uni_stanford, uni_oxford, uni_epfl])
    db.commit()
    db.refresh(uni_eth)
    db.refresh(uni_tum)
    db.refresh(uni_cmu)
    db.refresh(uni_stanford)
    db.refresh(uni_oxford)
    db.refresh(uni_epfl)

    # Programs
    prog_eth = Program(
        university_id=uni_eth.id,
        name="Master of Science in Computer Science (Major in Machine Intelligence)",
        degree="Master of Science (M.Sc.)",
        duration_semesters=4,
        language="English",
        application_deadline="15 December (Non-Bologna) / 31 March (Bologna)",
        gpa_requirement="Top 5% of class (approx 3.7+ / 4.0 or German 1.4)",
        gre_requirement="Mandatory for non-EU/EFTA applicants (Target: Q 166+, V 156+, AW 4.0)",
        language_requirement="TOEFL iBT 100+ or IELTS Academic 7.5+",
        scholarship_opportunities="ETH Excellence Scholarship & Opportunity Programme (ESOP)",
        credits_ects=120
    )
    prog_tum = Program(
        university_id=uni_tum.id,
        name="Master of Science in Informatics & Data Engineering",
        degree="Master of Science (M.Sc.)",
        duration_semesters=4,
        language="English",
        application_deadline="31 May (Winter Semester Intake)",
        gpa_requirement="German Grade 1.8 or higher (~3.5/4.0 GPA)",
        gre_requirement="GRE General recommended for international qualification",
        language_requirement="English B2/C1, IELTS 6.5+ or TOEFL 88+",
        scholarship_opportunities="DAAD Scholarships / TUM Deutschlandstipendium",
        credits_ects=120
    )
    prog_cmu = Program(
        university_id=uni_cmu.id,
        name="Master of Science in Machine Learning (MSML)",
        degree="Master of Science (M.S.)",
        duration_semesters=4,
        language="English",
        application_deadline="12 December",
        gpa_requirement="3.8+ / 4.0 with rigorous math & CS prerequisites",
        gre_requirement="Optional / Highly recommended (Quant 168+)",
        language_requirement="TOEFL 105+ (26+ per band) or IELTS 8.0",
        scholarship_opportunities="Graduate Research Assistantships (GRA) / Teaching Assistantships (TA)",
        credits_ects=144
    )
    db.add_all([prog_eth, prog_tum, prog_cmu])
    db.commit()
    db.refresh(prog_eth)
    db.refresh(prog_tum)
    db.refresh(prog_cmu)

    # Applications Pipeline
    app_eth = Application(
        user_id=user.id,
        university_id=uni_eth.id,
        program_id=prog_eth.id,
        status="Preparing",
        tier="Dream",
        deadline=datetime.datetime.utcnow() + datetime.timedelta(days=45),
        portal_url="https://e-apply.ethz.ch",
        application_fee_eur=150.0,
        notes="High priority. Need 3 academic recommendation letters highlighting strong mathematical foundations and independent research."
    )
    app_tum = Application(
        user_id=user.id,
        university_id=uni_tum.id,
        program_id=prog_tum.id,
        status="Shortlisted",
        tier="Target",
        deadline=datetime.datetime.utcnow() + datetime.timedelta(days=120),
        portal_url="https://campus.tum.de",
        application_fee_eur=80.0,
        notes="Aptitude assessment test requires detailed curricular analysis of mathematics and theoretical informatics credits."
    )
    app_cmu = Application(
        user_id=user.id,
        university_id=uni_cmu.id,
        program_id=prog_cmu.id,
        status="Researching",
        tier="Dream",
        deadline=datetime.datetime.utcnow() + datetime.timedelta(days=42),
        portal_url="https://scs.cmu.edu/admissions",
        application_fee_eur=125.0,
        notes="Identify 2 target research groups in MLD (Autonomous agents & Efficient Transformers)."
    )
    db.add_all([app_eth, app_tum, app_cmu])
    db.commit()
    db.refresh(app_eth)

    # Application Documents for ETH Zurich
    db.add_all([
        Document(application_id=app_eth.id, name="Statement of Purpose (SOP)", status="Drafting", notes="Draft 2 in progress: emphasizing ViT project and spectral graph theory work."),
        Document(application_id=app_eth.id, name="Academic CV (Europass / Standard CS)", status="Ready", notes="Reviewed by faculty advisor."),
        Document(application_id=app_eth.id, name="Official Undergrad Transcripts", status="Ready", notes="Sealed and verified digitally."),
        Document(application_id=app_eth.id, name="GRE Score Report (V158, Q169, AW4.5)", status="Ready", notes="Sent via ETS institutional code 3531."),
        Document(application_id=app_eth.id, name="Letter of Recommendation 1 (ML Lab Prof)", status="Submitted", notes="Confirmed submitted via portal."),
        Document(application_id=app_eth.id, name="Letter of Recommendation 2 (Math Dept Chair)", status="Review", notes="Drafted outline sent to professor."),
    ])

    # 9. Habits
    h1 = Habit(user_id=user.id, name="Deep Technical Study (2+ hrs)", category="Study", frequency="daily", target_days_per_week=7, current_streak=14, best_streak=28, color="indigo")
    h2 = Habit(user_id=user.id, name="Daily LeetCode Problem", category="Coding", frequency="daily", target_days_per_week=7, current_streak=12, best_streak=19, color="emerald")
    h3 = Habit(user_id=user.id, name="Math Derivation Practice", category="Math", frequency="daily", target_days_per_week=5, current_streak=8, best_streak=15, color="violet")
    h4 = Habit(user_id=user.id, name="ML Research Paper Reading", category="Research", frequency="daily", target_days_per_week=5, current_streak=6, best_streak=10, color="amber")
    h5 = Habit(user_id=user.id, name="Physical Exercise / Running", category="Health", frequency="daily", target_days_per_week=4, current_streak=4, best_streak=9, color="rose")
    h6 = Habit(user_id=user.id, name="Project Git Commit", category="Projects", frequency="daily", target_days_per_week=6, current_streak=11, best_streak=22, color="cyan")
    db.add_all([h1, h2, h3, h4, h5, h6])
    db.commit()
    db.refresh(h1)
    db.refresh(h2)

    # Generate realistic habit logs for the past 21 days
    today = datetime.date.today()
    for day_offset in range(21):
        log_date = (today - datetime.timedelta(days=day_offset)).isoformat()
        # Study habit (completed every day)
        db.add(HabitLog(habit_id=h1.id, date=log_date, completed=True, value=2.5))
        # Coding habit (completed 18 of 21 days)
        if day_offset not in [13, 17, 20]:
            db.add(HabitLog(habit_id=h2.id, date=log_date, completed=True, value=1.0))
        # Math habit
        if day_offset % 2 == 0:
            db.add(HabitLog(habit_id=h3.id, date=log_date, completed=True, value=1.0))
        # Research paper
        if day_offset % 3 != 0:
            db.add(HabitLog(habit_id=h4.id, date=log_date, completed=True, value=1.0))
    db.commit()

    # 10. Study Sessions (Past 7 days)
    for day_offset in range(7):
        session_time = datetime.datetime.utcnow() - datetime.timedelta(days=day_offset, hours=2)
        db.add(StudySession(
            user_id=user.id,
            subject="Mathematics",
            topic="Eigenvalues & Spectral Theorem",
            duration_minutes=50,
            session_type="pomodoro",
            completed_at=session_time,
            notes="Derived characteristic equation for 3x3 symmetric matrices.",
            focus_score=94.0
        ))
        db.add(StudySession(
            user_id=user.id,
            subject="Python",
            topic="NumPy Vectorization",
            duration_minutes=45,
            session_type="pomodoro",
            completed_at=session_time - datetime.timedelta(hours=2),
            notes="Benchmarked vector broadcasting against naive nested loops.",
            focus_score=92.0
        ))
        db.add(StudySession(
            user_id=user.id,
            subject="Machine Learning",
            topic="Loss Functions & Regularization",
            duration_minutes=60,
            session_type="deep_work",
            completed_at=session_time - datetime.timedelta(hours=4),
            notes="Implemented L1 Lasso soft-thresholding operator.",
            focus_score=88.0
        ))

    # 11. Goals & Hierarchy
    g_main = Goal(
        user_id=user.id,
        title="Become an Elite Machine Learning Research Engineer & Secure Top Tier Master's",
        description="Comprehensive 2-year trajectory: Build rigorous mathematical foundations, achieve LeetCode 300+ problem mastery, open source notable deep learning frameworks, and secure admission to ETH Zurich or TUM.",
        level="long_term",
        target_date=datetime.datetime.utcnow() + datetime.timedelta(days=730),
        progress=45.0,
        status="active"
    )
    db.add(g_main)
    db.commit()
    db.refresh(g_main)

    g_math = Goal(
        user_id=user.id,
        parent_goal_id=g_main.id,
        title="Master Graduate-Level Linear Algebra & Numerical Optimization",
        description="Complete all core problem sets in Gilbert Strang and Boyd & Vandenberghe.",
        level="yearly",
        target_date=datetime.datetime.utcnow() + datetime.timedelta(days=180),
        progress=72.0,
        status="active"
    )
    g_ml = Goal(
        user_id=user.id,
        parent_goal_id=g_main.id,
        title="Ship Vision Transformer & Autograd from Scratch with 90%+ Accuracy",
        description="Train, document, and publish technical write-up to demonstrate genuine internal architectural understanding.",
        level="quarterly",
        target_date=datetime.datetime.utcnow() + datetime.timedelta(days=60),
        progress=65.0,
        status="active"
    )
    g_app = Goal(
        user_id=user.id,
        parent_goal_id=g_main.id,
        title="Submit Complete Applications for ETH Zurich & TUM",
        description="Score high GRE (Q168+), craft tailored SOPs, and obtain 3 outstanding LORs.",
        level="quarterly",
        target_date=datetime.datetime.utcnow() + datetime.timedelta(days=45),
        progress=60.0,
        status="active"
    )
    db.add_all([g_math, g_ml, g_app])
    db.commit()

    # 12. AI Recommendations
    recs = [
        AIRecommendation(
            category="learning",
            title="Review gradients before neural-network optimization",
            recommendation="Your Jacobian & Hessian comprehension is at 82%, but you have not yet linked it to second-order Taylor approximations. Review curvature before implementing Adam and L-BFGS optimizers.",
            reason="Prerequisite graph indicates that second-order convergence analysis depends directly on Hessian matrix positive-definiteness.",
            action_label="Open Calculus Topic",
            action_route="/topic/" + str(t_math_calc.id),
            priority_score=0.98
        ),
        AIRecommendation(
            category="coding",
            title="Practice Topological Sort to eliminate Graph weakness",
            recommendation="You aced Course Schedule II, but Alien Dictionary tests tricky lexicographical prefixes. Tackling this will cement directed acyclic graph (DAG) mastery.",
            reason="Based on your recent graph attempt patterns, cycle detection with in-degrees is strong while string-to-graph translation needs one more challenge.",
            action_label="Solve Alien Dictionary",
            action_route="/coding",
            priority_score=0.92
        ),
        AIRecommendation(
            category="career",
            title="ETH Zurich Application Deadline in 45 Days",
            recommendation="The second Letter of Recommendation draft is currently awaiting review with your Mathematics Department Chair. Follow up this week to guarantee timely upload.",
            reason="Admissions portal records indicate early applicant cohorts undergo committee review in mid-January.",
            action_label="Review Application Pipeline",
            action_route="/masters",
            priority_score=0.95
        )
    ]
    db.add_all(recs)

    # 13. Achievements
    achievements = [
        Achievement(code="streak_14", title="Fortnight of Focus", description="Maintain an uninterrupted 14-day study streak", category="Streak", icon="flame", unlocked=True, unlocked_at=datetime.datetime.utcnow() - datetime.timedelta(days=1), progress_current=14, progress_max=14),
        Achievement(code="hours_200", title="Bicentennial Scholar", description="Surpass 200 cumulative hours of verified focused learning", category="Focus", icon="clock", unlocked=True, unlocked_at=datetime.datetime.utcnow() - datetime.timedelta(days=3), progress_current=216, progress_max=200),
        Achievement(code="matrix_master", title="Matrix Cartographer", description="Master all Linear Algebra foundational vectors and eigenvalue decompositions", category="Mastery", icon="sigma", unlocked=False, progress_current=3, progress_max=5),
        Achievement(code="problems_100", title="Algorithmic Century", description="Solve 100 data structures & algorithms challenges", category="Coding", icon="code", unlocked=False, progress_current=78, progress_max=100),
        Achievement(code="scratch_hero", title="First Principles Architect", description="Implement a machine learning algorithm completely from scratch in NumPy", category="Mastery", icon="cpu", unlocked=True, unlocked_at=datetime.datetime.utcnow() - datetime.timedelta(days=10), progress_current=1, progress_max=1),
        Achievement(code="global_bound", title="Global Scholar", description="Shortlist 5 world-class universities and commence application dossiers", category="Milestone", icon="compass", unlocked=True, unlocked_at=datetime.datetime.utcnow() - datetime.timedelta(days=12), progress_current=6, progress_max=5),
    ]
    db.add_all(achievements)

    # 14. Notifications
    notes_list = [
        Notification(user_id=user.id, title="Study streak active: 14 days!", message="Great discipline! Complete today's Linear Algebra task to reach day 15.", category="reminder"),
        Notification(user_id=user.id, title="Upcoming Application Milestone", message="ETH Zurich application fee payment window opens in 3 weeks.", category="deadline"),
        Notification(user_id=user.id, title="New AI Study Recommendation", message="Your customized daily study schedule is ready based on your 4.5h available time.", category="recommendation"),
    ]
    db.add_all(notes_list)

    # 15. Daily Plan
    dp = DailyPlan(
        user_id=user.id,
        date=str(today),
        available_hours=4.5,
        schedule_blocks=[
            {"time": "09:00 - 09:45", "duration_minutes": 45, "subject": "Mathematics", "topic": "Eigenvalues & Spectral Theorem", "type": "theory", "reason": "Weakest theoretical topic with high downstream impact on PCA and GNNs.", "difficulty": "Hard"},
            {"time": "09:50 - 10:35", "duration_minutes": 45, "subject": "Python", "topic": "NumPy Vectorized Strides", "type": "practice", "reason": "Build practical vectorization speed needed for from-scratch autograd.", "difficulty": "Medium"},
            {"time": "10:45 - 11:45", "duration_minutes": 60, "subject": "Machine Learning", "topic": "Ridge Regression Normal Equation", "type": "coding", "reason": "Direct algebraic bridge between matrix inversion and regularized loss.", "difficulty": "Medium"},
            {"time": "11:50 - 12:50", "duration_minutes": 60, "subject": "Coding", "topic": "Graph Topological Sort Problems", "type": "practice", "reason": "Reinforce DAG cycle detection algorithms for technical interviews.", "difficulty": "Hard"},
            {"time": "14:00 - 15:00", "duration_minutes": 60, "subject": "Master's Preparation", "topic": "ETH Zurich SOP Paragraph 3 Refinement", "type": "career", "reason": "Target deadline is approaching in 45 days.", "difficulty": "Medium"}
        ],
        daily_reflection_learned="Finally internalized why real symmetric matrices always have orthogonal eigenvectors via the Spectral Theorem.",
        daily_reflection_difficulty="Remembering the exact index manipulations in multi-dimensional numpy tensor broadcasting.",
        daily_reflection_review="Re-derive the Sherman-Morrison-Woodbury matrix inversion formula tomorrow morning.",
        daily_rating=5
    )
    db.add(dp)

    db.commit()
    db.close()
    print("StudyOS sample data successfully seeded!")

if __name__ == "__main__":
    init_db()
