import streamlit as st
import json
import datetime
from utils.ai_utils import generate_ai_response, stream_ai_response
from utils.sentiment_utils import analyze_sentiment_from_history
from utils.quiz_utils import generate_quiz_structured
from utils.notes_utils import generate_notes
from utils.roadmap_utils import generate_roadmap_structured
from utils.storage_utils import (
    load_session_data, save_session_data,
    get_chat_history, add_chat_message,
    get_study_plans, save_study_plan,
    get_quiz_sessions, save_quiz_session,
    update_study_plan_progress
)

# ─── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IntelliLearn AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root palette */
:root {
    --bg: #0e0f14;
    --surface: #16181f;
    --surface2: #1e2130;
    --border: #2a2d3e;
    --accent: #6c63ff;
    --accent2: #00d4aa;
    --accent3: #ff6b6b;
    --text: #e8eaf6;
    --muted: #7b7f9e;
    --radius: 12px;
}

/* Override Streamlit defaults */
.stApp { background: var(--bg); font-family: 'Sora', sans-serif; color: var(--text); }
.stSidebar { background: var(--surface) !important; border-right: 1px solid var(--border); }
.stSidebar [data-testid="stSidebarContent"] { padding: 1rem; }
.block-container { padding: 1.5rem 2rem; max-width: 1200px; }
h1,h2,h3,h4 { font-family: 'Sora', sans-serif; font-weight: 700; color: var(--text); }
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div { 
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
    font-family: 'Sora', sans-serif !important;
}
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Chat bubbles */
.chat-user {
    background: var(--accent);
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 16px 16px 4px 16px;
    margin: 0.5rem 0 0.5rem 15%;
    font-size: 0.9rem;
}
.chat-ai {
    background: var(--surface2);
    color: var(--text);
    padding: 0.75rem 1rem;
    border-radius: 16px 16px 16px 4px;
    margin: 0.5rem 15% 0.5rem 0;
    font-size: 0.9rem;
    border: 1px solid var(--border);
}
.chat-meta { font-size: 0.75rem; color: var(--muted); margin-top: 2px; }

/* Cards */
.il-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem;
    margin: 0.5rem 0;
    transition: border-color 0.2s;
}
.il-card:hover { border-color: var(--accent); }
.il-card-accent { border-left: 3px solid var(--accent); }

/* Nav tiles on home */
.nav-tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.nav-tile:hover { border-color: var(--accent); transform: translateY(-2px); }
.nav-tile .icon { font-size: 2rem; }
.nav-tile .label { font-weight: 600; margin-top: 0.5rem; color: var(--text); }
.nav-tile .desc { font-size: 0.8rem; color: var(--muted); margin-top: 0.25rem; }

/* Sentiment badge */
.badge-positive { background: #1a3d30; color: var(--accent2); padding: 3px 10px; border-radius: 20px; font-size: 0.8rem; }
.badge-negative { background: #3d1a1a; color: var(--accent3); padding: 3px 10px; border-radius: 20px; font-size: 0.8rem; }
.badge-neutral  { background: #2a2d3e; color: var(--muted); padding: 3px 10px; border-radius: 20px; font-size: 0.8rem; }

/* Quiz options */
.quiz-option {
    background: var(--surface2);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 0.75rem 1rem;
    margin: 0.35rem 0;
    cursor: pointer;
    transition: border-color 0.2s;
    font-size: 0.95rem;
}
.quiz-option:hover { border-color: var(--accent); }
.quiz-option-selected { border-color: var(--accent) !important; background: #1a1a3e !important; }
.quiz-option-correct { border-color: var(--accent2) !important; background: #0d2e26 !important; color: var(--accent2) !important; }
.quiz-option-wrong { border-color: var(--accent3) !important; background: #2e1515 !important; color: var(--accent3) !important; }

/* Progress bar */
.prog-bar { background: var(--border); border-radius: 99px; height: 8px; overflow: hidden; margin: 6px 0; }
.prog-fill { background: linear-gradient(90deg, var(--accent), var(--accent2)); height: 100%; border-radius: 99px; transition: width 0.5s; }

/* Metric card */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    text-align: center;
}
.metric-val { font-size: 2rem; font-weight: 700; color: var(--accent); font-family: 'JetBrains Mono', monospace; }
.metric-label { font-size: 0.8rem; color: var(--muted); }

/* Sidebar nav */
.sidebar-nav-item {
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    cursor: pointer;
    margin: 2px 0;
    font-size: 0.9rem;
    transition: background 0.15s;
}
.sidebar-nav-active { background: var(--accent) !important; color: white !important; }
.sidebar-nav-item:hover { background: var(--surface2); }

/* Roadmap milestone */
.milestone {
    display: flex;
    gap: 1rem;
    padding: 0.75rem 0;
    border-left: 2px solid var(--border);
    padding-left: 1rem;
    margin-left: 0.5rem;
    position: relative;
}
.milestone::before {
    content: '';
    width: 10px; height: 10px;
    background: var(--accent);
    border-radius: 50%;
    position: absolute;
    left: -6px;
    top: 1rem;
}
.milestone-done::before { background: var(--accent2); }

/* Divider */
.il-divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* Tag pills */
.tag { background: var(--surface2); color: var(--muted); padding: 2px 8px; border-radius: 20px; font-size: 0.75rem; margin: 2px; display: inline-block; }
.tag-accent { background: #1a1a3e; color: var(--accent); }

/* Stagger animation */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp 0.4s ease forwards; }
</style>
""", unsafe_allow_html=True)

# ─── Init session state ──────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "home",
        "chat_history": [],
        "quiz_state": None,
        "quiz_answers": {},
        "quiz_revealed": False,
        "study_plans": {},
        "active_plan_id": None,
        "notes_history": [],
        "learning_path": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Navigation helper ───────────────────────────────────────────────────────────
def nav_to(page):
    st.session_state.page = page
    st.rerun()

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0;'>
        <div style='font-size:2rem;'>🎓</div>
        <div style='font-size:1.1rem;font-weight:700;color:#e8eaf6;'>IntelliLearn AI</div>
        <div style='font-size:0.75rem;color:#7b7f9e;'>Education AI Solution</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    nav_items = [
        ("home", "🏠", "Home"),
        ("tutor", "🤖", "AI Tutor"),
        ("quiz", "❓", "Quiz Generator"),
        ("notes", "📝", "Notes Generator"),
        ("roadmap", "🗺️", "Study Roadmap"),
        ("dashboard", "📊", "My Dashboard"),
    ]
    
    for page_id, icon, label in nav_items:
        active = st.session_state.page == page_id
        style = "background:#6c63ff;color:white;" if active else "color:#e8eaf6;"
        if st.button(f"{icon}  {label}", key=f"nav_{page_id}", use_container_width=True):
            nav_to(page_id)
    
    st.divider()
    
    # Quick stats
    total_messages = len(st.session_state.chat_history)
    quiz_sessions = len([s for s in st.session_state.get("quiz_sessions_log", [])])
    plans = len(st.session_state.study_plans)
    
    st.markdown(f"""
    <div style='font-size:0.75rem;color:#7b7f9e;'>
        <div style='margin-bottom:6px;'>💬 {total_messages} chat messages</div>
        <div style='margin-bottom:6px;'>📚 {plans} study plan(s)</div>
        <div style='margin-bottom:6px;'>🎯 {len(st.session_state.get("quiz_sessions_log",[]))} quiz session(s)</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Page: HOME ─────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    
    st.markdown("""
    <div style='padding: 2rem 0 1rem;'>
        <h1 style='font-size:2.5rem;margin-bottom:0.25rem;'>
            Welcome to <span style='color:#6c63ff;'>IntelliLearn AI</span>
        </h1>
        <p style='color:#7b7f9e;font-size:1rem;margin-top:0;'>
            Your personal AI-powered learning companion — study smarter, track progress, master anything.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sentiment summary from chat
    if len(st.session_state.chat_history) >= 2:
        sentiment_result = analyze_sentiment_from_history(st.session_state.chat_history)
        s = sentiment_result["overall"]
        badge_class = f"badge-{s.lower()}"
        st.markdown(f"""
        <div class='il-card' style='display:flex;align-items:center;gap:1rem;padding:0.75rem 1.25rem;margin-bottom:1rem;'>
            <span style='font-size:1.2rem;'>🧠</span>
            <span style='color:#7b7f9e;font-size:0.9rem;'>Learning sentiment from your sessions:</span>
            <span class='{badge_class}'>{s}</span>
            <span style='color:#7b7f9e;font-size:0.8rem;margin-left:auto;'>{sentiment_result["summary"]}</span>
        </div>
        """, unsafe_allow_html=True)

    # Optional: preset learning path
    if st.session_state.learning_path:
        st.markdown(f"""
        <div class='il-card il-card-accent' style='margin-bottom:1rem;'>
            <div style='display:flex;align-items:center;gap:0.75rem;'>
                <span style='font-size:1.2rem;'>🎯</span>
                <div>
                    <div style='font-weight:600;'>Active Learning Path: {st.session_state.learning_path["name"]}</div>
                    <div style='font-size:0.8rem;color:#7b7f9e;'>{st.session_state.learning_path["description"]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Feature tiles
    st.markdown("<div style='margin-bottom:0.75rem;font-weight:600;color:#7b7f9e;font-size:0.85rem;letter-spacing:0.08em;'>QUICK ACCESS</div>", unsafe_allow_html=True)
    
    tiles = [
        ("tutor", "🤖", "AI Tutor", "Ask questions, get explanations with examples & analogies"),
        ("quiz", "❓", "Quiz Generator", "Test your knowledge with interactive AI-generated quizzes"),
        ("notes", "📝", "Notes Generator", "Convert any content into structured study notes"),
        ("roadmap", "🗺️", "Study Roadmap", "Get a personalised week-by-week learning plan"),
        ("dashboard", "📊", "My Dashboard", "Track progress, sentiment & quiz performance"),
    ]
    
    cols = st.columns(3)
    for i, (page_id, icon, label, desc) in enumerate(tiles):
        with cols[i % 3]:
            if st.button(f"{icon}\n\n**{label}**\n\n{desc}", key=f"tile_{page_id}", use_container_width=True):
                nav_to(page_id)
    
    st.markdown("<hr class='il-divider'>", unsafe_allow_html=True)
    
    # Learning path selector
    st.markdown("### 🎯 Choose a Learning Path")
    st.markdown("<p style='color:#7b7f9e;font-size:0.9rem;'>Select a preset path to focus your AI Tutor, Quizzes and Roadmaps.</p>", unsafe_allow_html=True)
    
    LEARNING_PATHS = {
        "Python for Data Science": {
            "name": "Python for Data Science",
            "description": "Master Python fundamentals, data manipulation with pandas, and visualisation",
            "topics": ["Python basics", "NumPy", "Pandas", "Matplotlib", "Data cleaning"],
            "emoji": "🐍"
        },
        "Machine Learning Foundations": {
            "name": "Machine Learning Foundations",
            "description": "Supervised & unsupervised learning, model evaluation, and scikit-learn",
            "topics": ["Regression", "Classification", "Clustering", "Model evaluation", "Feature engineering"],
            "emoji": "🤖"
        },
        "Generative AI & Prompt Engineering": {
            "name": "Generative AI & Prompt Engineering",
            "description": "LLMs, prompt design, RAG, and building AI-powered applications",
            "topics": ["LLMs", "Prompt engineering", "RAG", "Embeddings", "AI APIs"],
            "emoji": "✨"
        },
        "AI for Business & Everyone": {
            "name": "AI for Business & Everyone",
            "description": "Non-technical overview of AI concepts, ethics, and real-world applications",
            "topics": ["AI fundamentals", "Use cases", "Responsible AI", "AI strategy", "Tools overview"],
            "emoji": "💼"
        },
        "Natural Language Processing": {
            "name": "Natural Language Processing",
            "description": "Text preprocessing, sentiment analysis, transformers, and NLP pipelines",
            "topics": ["Tokenisation", "Sentiment analysis", "Named entity recognition", "Transformers", "BERT"],
            "emoji": "📖"
        },
        "Custom": {
            "name": "Custom",
            "description": "Define your own topic focus",
            "topics": [],
            "emoji": "🛠️"
        }
    }
    
    path_cols = st.columns(3)
    for i, (k, v) in enumerate(LEARNING_PATHS.items()):
        with path_cols[i % 3]:
            active = st.session_state.learning_path and st.session_state.learning_path["name"] == v["name"]
            btn_label = f"{v['emoji']} {v['name']}" + (" ✓" if active else "")
            if st.button(btn_label, key=f"path_{k}", use_container_width=True):
                if k == "Custom":
                    st.session_state.learning_path = None
                    st.session_state._show_custom_path = True
                else:
                    st.session_state.learning_path = v
                    st.session_state._show_custom_path = False
                st.rerun()
    
    if st.session_state.get("_show_custom_path") or (st.session_state.learning_path and st.session_state.learning_path["name"] == "Custom"):
        custom_name = st.text_input("Path name", key="custom_path_name")
        custom_desc = st.text_input("What do you want to learn?", key="custom_path_desc")
        if st.button("Set Custom Path") and custom_name:
            st.session_state.learning_path = {"name": custom_name, "description": custom_desc, "topics": [], "emoji": "🛠️"}
            st.session_state._show_custom_path = False
            st.rerun()
    
    if st.session_state.learning_path:
        if st.button("✕ Clear Learning Path"):
            st.session_state.learning_path = None
            st.rerun()

# ─── Page: AI TUTOR ─────────────────────────────────────────────────────────────
elif st.session_state.page == "tutor":
    
    st.markdown("""
    <h1>🤖 AI Tutor</h1>
    <p style='color:#7b7f9e;'>Ask me anything — I explain with clarity, examples, and real-world analogies.</p>
    """, unsafe_allow_html=True)
    
    # Show active learning path context
    if st.session_state.learning_path:
        lp = st.session_state.learning_path
        st.markdown(f"""
        <div class='il-card' style='padding:0.6rem 1rem;margin-bottom:1rem;display:flex;align-items:center;gap:0.5rem;'>
            <span>{lp['emoji']}</span>
            <span style='font-size:0.85rem;color:#7b7f9e;'>Learning path: <span style='color:#6c63ff;'>{lp['name']}</span></span>
        </div>
        """, unsafe_allow_html=True)
    
    # Render chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                sentiment = msg.get("sentiment", "")
                badge = ""
                if sentiment:
                    bc = f"badge-{sentiment.lower()}"
                    badge = f"<span class='{bc}' style='float:right;font-size:0.7rem;'>{sentiment}</span>"
                st.markdown(f"<div class='chat-ai'>{badge}{msg['content']}</div>", unsafe_allow_html=True)
    
    # Quick suggestion chips based on learning path
    if st.session_state.learning_path and st.session_state.learning_path.get("topics"):
        st.markdown("<div style='margin:0.5rem 0;font-size:0.8rem;color:#7b7f9e;'>Suggested topics:</div>", unsafe_allow_html=True)
        chip_cols = st.columns(len(st.session_state.learning_path["topics"][:5]))
        for i, topic in enumerate(st.session_state.learning_path["topics"][:5]):
            with chip_cols[i]:
                if st.button(topic, key=f"chip_{i}"):
                    st.session_state._prefill_question = f"Explain {topic} to me as a beginner"
                    st.rerun()
    
    # Input area
    prefill = st.session_state.pop("_prefill_question", "") if "_prefill_question" in st.session_state else ""
    user_input = st.text_input(
        "Ask a question...",
        value=prefill,
        placeholder="e.g. What is gradient descent? How does attention work in transformers?",
        key="tutor_input"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        send = st.button("Send ➤", key="tutor_send")
    with col2:
        if st.button("Clear Chat 🗑️", key="tutor_clear"):
            st.session_state.chat_history = []
            st.rerun()
    
    if send and user_input.strip():
        # Analyze sentiment of user message
        from utils.sentiment_utils import analyze_text_sentiment
        user_sentiment = analyze_text_sentiment(user_input)
        
        # Build system context
        system_context = "You are IntelliLearn AI, a friendly and clear educational tutor. Always explain with: 1) a simple explanation, 2) a concrete example, 3) a real-world analogy. Keep responses concise but thorough."
        if st.session_state.learning_path:
            system_context += f" The student is focused on: {st.session_state.learning_path['name']} — {st.session_state.learning_path['description']}."
        
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "sentiment": user_sentiment["sentiment"],
            "timestamp": str(datetime.datetime.now())
        })
        
        # Build conversation for API
        messages = []
        for m in st.session_state.chat_history[-10:]:
            messages.append({"role": m["role"], "content": m["content"]})
        
        with st.spinner("Thinking..."):
            response = generate_ai_response(messages, system=system_context)
        
        ai_sentiment = analyze_text_sentiment(response)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "sentiment": ai_sentiment["sentiment"],
            "timestamp": str(datetime.datetime.now())
        })
        st.rerun()

# ─── Page: QUIZ ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "quiz":
    
    st.markdown("""
    <h1>❓ Quiz Generator</h1>
    <p style='color:#7b7f9e;'>Test your understanding with AI-generated multiple-choice questions. Answer first, then reveal results.</p>
    """, unsafe_allow_html=True)
    
    # Quiz setup
    with st.expander("⚙️ Generate New Quiz", expanded=st.session_state.quiz_state is None):
        
        lp_default = ""
        if st.session_state.learning_path:
            lp_default = st.session_state.learning_path["name"]
        
        topic = st.text_input("Topic", value=lp_default, placeholder="e.g. Neural Networks, Python lists, Gradient Descent")
        num_q = st.slider("Number of questions", 3, 10, 5)
        difficulty = st.select_slider("Difficulty", ["Beginner", "Intermediate", "Advanced"], "Intermediate")
        
        if st.button("🎲 Generate Quiz", key="gen_quiz"):
            with st.spinner(f"Creating {num_q} questions on '{topic}'..."):
                quiz_data = generate_quiz_structured(topic, num_q, difficulty)
            if quiz_data:
                st.session_state.quiz_state = quiz_data
                st.session_state.quiz_answers = {}
                st.session_state.quiz_revealed = False
                st.session_state._quiz_topic = topic
                st.session_state._quiz_difficulty = difficulty
                st.rerun()
    
    # Render active quiz
    if st.session_state.quiz_state:
        questions = st.session_state.quiz_state
        answered = len(st.session_state.quiz_answers)
        total = len(questions)
        
        # Progress bar
        pct = int(answered / total * 100) if total else 0
        st.markdown(f"""
        <div style='margin:1rem 0;'>
            <div style='display:flex;justify-content:space-between;font-size:0.8rem;color:#7b7f9e;margin-bottom:4px;'>
                <span>Progress</span><span>{answered}/{total} answered</span>
            </div>
            <div class='prog-bar'><div class='prog-fill' style='width:{pct}%;'></div></div>
        </div>
        """, unsafe_allow_html=True)
        
        revealed = st.session_state.quiz_revealed
        
        for qi, q in enumerate(questions):
            st.markdown(f"""
            <div class='il-card' style='margin:1rem 0;'>
                <div style='font-weight:600;margin-bottom:0.75rem;'>
                    <span style='color:#7b7f9e;font-family:JetBrains Mono,monospace;'>Q{qi+1}.</span> {q['question']}
                </div>
            """, unsafe_allow_html=True)
            
            user_ans = st.session_state.quiz_answers.get(qi)
            correct_ans = q.get("answer", "")
            
            for oi, option in enumerate(q["options"]):
                opt_label = option
                is_selected = user_ans == oi
                is_correct_opt = revealed and (option.strip().startswith(correct_ans) or opt_label == correct_ans)
                is_wrong = revealed and is_selected and not is_correct_opt
                
                extra_style = ""
                if revealed and is_correct_opt:
                    extra_style = "border-color:#00d4aa !important;background:#0d2e26 !important;color:#00d4aa !important;"
                elif revealed and is_wrong:
                    extra_style = "border-color:#ff6b6b !important;background:#2e1515 !important;color:#ff6b6b !important;"
                elif is_selected:
                    extra_style = "border-color:#6c63ff !important;background:#1a1a3e !important;"
                
                if not revealed:
                    if st.button(f"  {option}", key=f"q{qi}_o{oi}", use_container_width=True):
                        st.session_state.quiz_answers[qi] = oi
                        st.rerun()
                else:
                    st.markdown(f"<div class='quiz-option' style='{extra_style}'>{option}</div>", unsafe_allow_html=True)
            
            if revealed and q.get("explanation"):
                st.markdown(f"<div style='margin-top:0.5rem;font-size:0.85rem;color:#7b7f9e;padding:0.5rem;background:#1e2130;border-radius:8px;'>💡 {q['explanation']}</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if not revealed:
                if st.button("🔍 Reveal Answers", key="reveal_answers"):
                    st.session_state.quiz_revealed = True
                    # Log quiz session
                    correct_count = sum(
                        1 for qi2, q2 in enumerate(questions)
                        if st.session_state.quiz_answers.get(qi2) is not None and
                        questions[qi2]["options"][st.session_state.quiz_answers[qi2]].strip().startswith(q2.get("answer",""))
                    )
                    log = st.session_state.get("quiz_sessions_log", [])
                    log.append({
                        "topic": st.session_state.get("_quiz_topic",""),
                        "difficulty": st.session_state.get("_quiz_difficulty",""),
                        "score": correct_count,
                        "total": total,
                        "date": str(datetime.date.today())
                    })
                    st.session_state.quiz_sessions_log = log
                    # Also save to chat history as a sentiment datapoint
                    score_pct = int(correct_count / total * 100) if total else 0
                    feeling = "great" if score_pct >= 70 else ("okay" if score_pct >= 40 else "struggling")
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": f"I just completed a quiz on {st.session_state.get('_quiz_topic','')} and scored {correct_count}/{total} ({score_pct}%). I feel {feeling} about it.",
                        "sentiment": "Positive" if score_pct >= 70 else ("Neutral" if score_pct >= 40 else "Negative"),
                        "timestamp": str(datetime.datetime.now()),
                        "_quiz_entry": True
                    })
                    st.rerun()
            else:
                correct_count = sum(
                    1 for qi2, q2 in enumerate(questions)
                    if st.session_state.quiz_answers.get(qi2) is not None and
                    questions[qi2]["options"][st.session_state.quiz_answers[qi2]].strip().startswith(q2.get("answer",""))
                )
                score_pct = int(correct_count / total * 100) if total else 0
                emoji = "🎉" if score_pct >= 70 else ("👍" if score_pct >= 40 else "💪")
                st.markdown(f"""
                <div style='text-align:center;padding:1rem;background:#1e2130;border-radius:12px;'>
                    <div style='font-size:2rem;'>{emoji}</div>
                    <div style='font-size:1.5rem;font-weight:700;color:#6c63ff;'>{score_pct}%</div>
                    <div style='color:#7b7f9e;font-size:0.9rem;'>{correct_count} / {total} correct</div>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            if st.button("🔄 New Quiz"):
                st.session_state.quiz_state = None
                st.session_state.quiz_answers = {}
                st.session_state.quiz_revealed = False
                st.rerun()
        
        # Previous sessions
        if st.session_state.get("quiz_sessions_log"):
            st.markdown("<hr class='il-divider'>", unsafe_allow_html=True)
            st.markdown("#### 📈 Quiz History")
            for sess in reversed(st.session_state.quiz_sessions_log[-5:]):
                pct2 = int(sess["score"] / sess["total"] * 100) if sess["total"] else 0
                color = "#00d4aa" if pct2 >= 70 else ("#6c63ff" if pct2 >= 40 else "#ff6b6b")
                st.markdown(f"""
                <div class='il-card' style='display:flex;align-items:center;gap:1rem;padding:0.6rem 1rem;'>
                    <div style='flex:1;'>
                        <div style='font-weight:600;font-size:0.9rem;'>{sess["topic"]}</div>
                        <div style='font-size:0.75rem;color:#7b7f9e;'>{sess["date"]} · {sess["difficulty"]}</div>
                    </div>
                    <div style='font-size:1.1rem;font-weight:700;color:{color};font-family:JetBrains Mono,monospace;'>{pct2}%</div>
                </div>
                """, unsafe_allow_html=True)

# ─── Page: NOTES ────────────────────────────────────────────────────────────────
elif st.session_state.page == "notes":
    
    st.markdown("""
    <h1>📝 Notes Generator</h1>
    <p style='color:#7b7f9e;'>Paste any content — textbooks, lecture slides, articles — and get structured study notes instantly.</p>
    """, unsafe_allow_html=True)
    
    if st.session_state.learning_path:
        lp = st.session_state.learning_path
        st.markdown(f"<div class='tag tag-accent'>{lp['emoji']} {lp['name']}</div>", unsafe_allow_html=True)
    
    notes_input = st.text_area(
        "Paste your content here",
        height=200,
        placeholder="Paste lecture notes, textbook passages, or any learning material..."
    )
    
    format_choice = st.selectbox("Output format", ["Structured bullet points", "Summary + Key Concepts", "Flashcard-style Q&A", "Mind map outline"])
    
    if st.button("⚡ Generate Notes", key="gen_notes"):
        if notes_input.strip():
            with st.spinner("Generating notes..."):
                notes = generate_notes(notes_input, format_choice, st.session_state.learning_path)
            st.session_state.notes_history.append({
                "input": notes_input[:100] + "...",
                "output": notes,
                "format": format_choice,
                "date": str(datetime.date.today())
            })
            st.markdown("<hr class='il-divider'>", unsafe_allow_html=True)
            st.markdown(notes)
        else:
            st.warning("Please paste some content first.")
    
    if st.session_state.notes_history:
        st.markdown("<hr class='il-divider'>", unsafe_allow_html=True)
        st.markdown("#### 📚 Recent Notes")
        for n in reversed(st.session_state.notes_history[-3:]):
            with st.expander(f"{n['format']} · {n['date']}"):
                st.markdown(n["output"])

# ─── Page: ROADMAP ──────────────────────────────────────────────────────────────
elif st.session_state.page == "roadmap":
    
    st.markdown("""
    <h1>🗺️ Study Roadmap</h1>
    <p style='color:#7b7f9e;'>Generate a personalised week-by-week learning plan and track your progress.</p>
    """, unsafe_allow_html=True)
    
    # Generate new plan
    with st.expander("➕ Create New Study Plan", expanded=len(st.session_state.study_plans) == 0):
        
        lp_default = ""
        if st.session_state.learning_path:
            lp_default = st.session_state.learning_path["description"]
        
        goal = st.text_input("Learning goal", value=lp_default, placeholder="e.g. Learn machine learning in 4 weeks, Master Python for data science")
        weeks = st.slider("Duration (weeks)", 2, 12, 4)
        hours = st.slider("Hours per week available", 2, 30, 10)
        
        if st.button("🗺️ Generate Roadmap", key="gen_roadmap"):
            if goal.strip():
                with st.spinner("Building your personalised roadmap..."):
                    roadmap = generate_roadmap_structured(goal, weeks, hours, st.session_state.learning_path)
                
                plan_id = f"plan_{len(st.session_state.study_plans)+1}_{datetime.date.today()}"
                st.session_state.study_plans[plan_id] = {
                    "id": plan_id,
                    "goal": goal,
                    "weeks": roadmap,
                    "created": str(datetime.date.today()),
                    "progress": {}  # {week_idx: {milestone_idx: bool}}
                }
                st.session_state.active_plan_id = plan_id
                st.rerun()
    
    # Show plans
    if not st.session_state.study_plans:
        st.markdown("""
        <div class='il-card' style='text-align:center;padding:3rem;'>
            <div style='font-size:3rem;'>🗺️</div>
            <div style='color:#7b7f9e;margin-top:0.5rem;'>No study plans yet. Create your first one above!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Plan selector
        plan_ids = list(st.session_state.study_plans.keys())
        
        if len(plan_ids) > 1:
            selected_label = st.selectbox(
                "Select plan",
                plan_ids,
                format_func=lambda x: f"{st.session_state.study_plans[x]['goal'][:50]} ({st.session_state.study_plans[x]['created']})",
                index=plan_ids.index(st.session_state.active_plan_id) if st.session_state.active_plan_id in plan_ids else 0
            )
            st.session_state.active_plan_id = selected_label
        
        plan = st.session_state.study_plans.get(st.session_state.active_plan_id or plan_ids[0])
        if not plan:
            plan = st.session_state.study_plans[plan_ids[0]]
            st.session_state.active_plan_id = plan_ids[0]
        
        # Overall progress
        all_milestones = sum(len(w.get("milestones", [])) for w in plan["weeks"])
        completed_milestones = sum(
            sum(1 for v in week_prog.values() if v)
            for week_prog in plan["progress"].values()
        )
        overall_pct = int(completed_milestones / all_milestones * 100) if all_milestones else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><div class='metric-val'>{overall_pct}%</div><div class='metric-label'>Overall Progress</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div class='metric-val'>{completed_milestones}</div><div class='metric-label'>Milestones Done</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><div class='metric-val'>{len(plan['weeks'])}</div><div class='metric-label'>Total Weeks</div></div>", unsafe_allow_html=True)
        
        st.markdown("<hr class='il-divider'>", unsafe_allow_html=True)
        
        # Render weeks
        for wi, week in enumerate(plan["weeks"]):
            week_prog = plan["progress"].get(str(wi), {})
            week_done = sum(1 for v in week_prog.values() if v)
            week_total = len(week.get("milestones", []))
            week_pct = int(week_done / week_total * 100) if week_total else 0
            
            with st.expander(f"📅 Week {wi+1}: {week.get('theme', '')} — {week_pct}% complete", expanded=wi == 0):
                st.markdown(f"<p style='color:#7b7f9e;font-size:0.9rem;'>{week.get('description','')}</p>", unsafe_allow_html=True)
                
                for mi, milestone in enumerate(week.get("milestones", [])):
                    is_done = week_prog.get(str(mi), False)
                    check = "✅" if is_done else "⬜"
                    cols = st.columns([0.08, 0.92])
                    with cols[0]:
                        if st.button(check, key=f"ms_{wi}_{mi}"):
                            if str(wi) not in plan["progress"]:
                                plan["progress"][str(wi)] = {}
                            plan["progress"][str(wi)][str(mi)] = not is_done
                            st.rerun()
                    with cols[1]:
                        style = "text-decoration:line-through;color:#7b7f9e;" if is_done else ""
                        st.markdown(f"<div style='{style};padding-top:4px;font-size:0.9rem;'>{milestone}</div>", unsafe_allow_html=True)
                
                if week.get("project"):
                    st.markdown(f"""
                    <div style='margin-top:0.75rem;padding:0.75rem;background:#1a1a3e;border-radius:8px;border-left:3px solid #6c63ff;'>
                        <div style='font-size:0.8rem;color:#7b7f9e;'>🔨 Mini Project</div>
                        <div style='font-size:0.9rem;'>{week['project']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        if st.button("🗑️ Delete this plan", key="del_plan"):
            del st.session_state.study_plans[plan["id"]]
            st.session_state.active_plan_id = None
            st.rerun()

# ─── Page: DASHBOARD ────────────────────────────────────────────────────────────
elif st.session_state.page == "dashboard":
    
    st.markdown("""
    <h1>📊 My Dashboard</h1>
    <p style='color:#7b7f9e;'>Your real learning analytics — built from your actual sessions.</p>
    """, unsafe_allow_html=True)
    
    # Compute stats from actual data
    total_messages = len([m for m in st.session_state.chat_history if m["role"] == "user" and not m.get("_quiz_entry")])
    quiz_logs = st.session_state.get("quiz_sessions_log", [])
    avg_score = int(sum(q["score"]/q["total"]*100 for q in quiz_logs) / len(quiz_logs)) if quiz_logs else 0
    
    all_milestones = sum(len(w.get("milestones", [])) for p in st.session_state.study_plans.values() for w in p["weeks"])
    completed_milestones = sum(
        sum(1 for v in wp.values() if v)
        for p in st.session_state.study_plans.values()
        for wp in p["progress"].values()
    )
    
    # Sentiment from chat
    if st.session_state.chat_history:
        sentiment_data = analyze_sentiment_from_history(st.session_state.chat_history)
    else:
        sentiment_data = {"overall": "N/A", "positive": 0, "negative": 0, "neutral": 0, "summary": "No sessions yet"}
    
    # Metric row
    cols = st.columns(4)
    metrics = [
        ("💬", "Chat Messages", total_messages),
        ("🎯", "Quiz Sessions", len(quiz_logs)),
        ("🏆", "Avg Quiz Score", f"{avg_score}%" if quiz_logs else "N/A"),
        ("✅", "Milestones Done", f"{completed_milestones}/{all_milestones}" if all_milestones else "0"),
    ]
    for i, (icon, label, val) in enumerate(metrics):
        with cols[i]:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:1.5rem;'>{icon}</div>
                <div class='metric-val' style='font-size:1.5rem;'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr class='il-divider'>", unsafe_allow_html=True)
    
    # Sentiment analysis from conversations
    st.markdown("### 🧠 Learning Sentiment Analysis")
    st.markdown("<p style='color:#7b7f9e;font-size:0.85rem;'>Derived from your actual AI Tutor conversations and quiz results.</p>", unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
        <div class='il-card' style='text-align:center;padding:2rem;'>
            <div style='font-size:2rem;'>💬</div>
            <div style='color:#7b7f9e;margin-top:0.5rem;'>Start a conversation in the AI Tutor tab to see your sentiment analysis here.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        pos = sentiment_data["positive"]
        neg = sentiment_data["negative"]
        neu = sentiment_data["neutral"]
        total_s = pos + neg + neu or 1
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"""
            <div class='il-card'>
                <div style='font-weight:600;margin-bottom:1rem;'>Overall Mood</div>
                <div style='font-size:2.5rem;font-weight:700;color:{"#00d4aa" if sentiment_data["overall"]=="Positive" else "#ff6b6b" if sentiment_data["overall"]=="Negative" else "#7b7f9e"};'>
                    {sentiment_data["overall"]}
                </div>
                <div style='color:#7b7f9e;font-size:0.85rem;margin-top:0.5rem;'>{sentiment_data["summary"]}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            for label, count, color in [("Positive", pos, "#00d4aa"), ("Neutral", neu, "#7b7f9e"), ("Negative", neg, "#ff6b6b")]:
                pct_s = int(count / total_s * 100)
                st.markdown(f"""
                <div style='margin:0.5rem 0;'>
                    <div style='display:flex;justify-content:space-between;font-size:0.8rem;color:#7b7f9e;'>
                        <span style='color:{color};'>{label}</span><span>{pct_s}%</span>
                    </div>
                    <div class='prog-bar'><div style='height:100%;background:{color};border-radius:99px;width:{pct_s}%;'></div></div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<hr class='il-divider'>", unsafe_allow_html=True)
    
    # Quiz performance
    st.markdown("### 🎯 Quiz Performance")
    if not quiz_logs:
        st.markdown("<div style='color:#7b7f9e;'>No quiz sessions yet. Try the Quiz Generator!</div>", unsafe_allow_html=True)
    else:
        for q in reversed(quiz_logs[-5:]):
            pct_q = int(q["score"]/q["total"]*100)
            color_q = "#00d4aa" if pct_q >= 70 else ("#6c63ff" if pct_q >= 40 else "#ff6b6b")
            st.markdown(f"""
            <div class='il-card' style='display:flex;align-items:center;gap:1rem;padding:0.75rem 1.25rem;'>
                <div style='flex:1;'>
                    <div style='font-weight:600;'>{q["topic"]}</div>
                    <div style='font-size:0.75rem;color:#7b7f9e;'>{q["date"]} · {q["difficulty"]}</div>
                    <div class='prog-bar' style='margin-top:6px;'><div style='height:100%;background:{color_q};border-radius:99px;width:{pct_q}%;'></div></div>
                </div>
                <div style='font-size:1.3rem;font-weight:700;color:{color_q};font-family:JetBrains Mono,monospace;'>{pct_q}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr class='il-divider'>", unsafe_allow_html=True)
    
    # Study plan progress
    st.markdown("### 🗺️ Study Plan Progress")
    if not st.session_state.study_plans:
        st.markdown("<div style='color:#7b7f9e;'>No study plans yet. Create one in the Study Roadmap tab!</div>", unsafe_allow_html=True)
    else:
        for pid, plan in st.session_state.study_plans.items():
            all_ms = sum(len(w.get("milestones", [])) for w in plan["weeks"])
            done_ms = sum(sum(1 for v in wp.values() if v) for wp in plan["progress"].values())
            p_pct = int(done_ms / all_ms * 100) if all_ms else 0
            st.markdown(f"""
            <div class='il-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <div style='font-weight:600;'>{plan["goal"][:60]}</div>
                        <div style='font-size:0.75rem;color:#7b7f9e;'>Created {plan["created"]} · {len(plan["weeks"])} weeks</div>
                    </div>
                    <div style='font-size:1.3rem;font-weight:700;color:#6c63ff;font-family:JetBrains Mono,monospace;'>{p_pct}%</div>
                </div>
                <div class='prog-bar' style='margin-top:8px;'><div class='prog-fill' style='width:{p_pct}%;'></div></div>
            </div>
            """, unsafe_allow_html=True)
