"""Generate all documentation diagrams as PNG images."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT = "/home/claude/intellilearn-ai/docs/images"
os.makedirs(OUT, exist_ok=True)

BG = "#0e0f14"
SURFACE = "#16181f"
SURFACE2 = "#1e2130"
BORDER = "#2a2d3e"
ACCENT = "#6c63ff"
ACCENT2 = "#00d4aa"
ACCENT3 = "#ff6b6b"
TEXT = "#e8eaf6"
MUTED = "#7b7f9e"


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {name}.png")


# ─── 1. ARCHITECTURE DIAGRAM ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

ax.text(7, 8.5, "IntelliLearn AI — System Architecture", ha='center', va='center',
        fontsize=16, fontweight='bold', color=TEXT)

# Layers
layers = [
    (1, 6.5, 12, 1.2, SURFACE, ACCENT, "Presentation Layer (Streamlit UI)", 
     "Home  ·  AI Tutor  ·  Quiz Generator  ·  Notes  ·  Study Roadmap  ·  Dashboard"),
    (1, 4.8, 12, 1.2, SURFACE, ACCENT2, "Application / Business Logic Layer",
     "Sentiment Analysis  ·  Quiz Engine  ·  Notes Engine  ·  Roadmap Generator  ·  Session State Manager"),
    (1, 3.1, 12, 1.2, SURFACE, "#6c63ff", "AI Integration Layer",
     "ai_utils.py  ·  Groq API Client  ·  Prompt Templates  ·  Multi-turn Conversation Manager"),
    (1, 1.4, 5.5, 1.2, SURFACE, ACCENT3, "Data Layer",
     "Session State  ·  Chat History  ·  Quiz Logs  ·  Study Plans"),
    (7.5, 1.4, 5.5, 1.2, SURFACE, MUTED, "External Services",
     "Groq API (LLaMA 3.1)  ·  VADER Sentiment  ·  .env Config"),
]

for x, y, w, h, fc, ec, title, sub in layers:
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                          facecolor=fc, edgecolor=ec, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.65, title, ha='center', va='center',
            fontsize=10, fontweight='bold', color=ec)
    ax.text(x + w/2, y + h*0.25, sub, ha='center', va='center',
            fontsize=7.5, color=MUTED)

# Arrows
for ay in [6.5, 4.8, 3.1]:
    ax.annotate("", xy=(7, ay), xytext=(7, ay - 0.1),
                arrowprops=dict(arrowstyle="<->", color=BORDER, lw=1.5))

save(fig, "architecture_diagram")


# ─── 2. UML CLASS DIAGRAM ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(8, 9.6, "UML Class Diagram — IntelliLearn AI", ha='center', fontsize=15,
        fontweight='bold', color=TEXT)

classes = [
    # x, y, w, h, name, attrs, methods
    (0.3, 6.0, 4.5, 3.5, "App (app.py)", 
     ["session_state: dict", "learning_path: dict | None", "chat_history: list", "study_plans: dict"],
     ["init_state()", "nav_to(page)", "render_home()", "render_tutor()", "render_quiz()", "render_roadmap()", "render_dashboard()"]),
    (5.5, 7.5, 4.5, 1.8, "AIUtils",
     ["MODEL: str", "client: Groq"],
     ["generate_ai_response(msgs, sys)", "simple_prompt(text)", "stream_ai_response(msgs)"]),
    (5.5, 5.0, 4.5, 2.2, "SentimentUtils",
     ["analyzer: VADER"],
     ["analyze_text_sentiment(text): dict", "analyze_sentiment_from_history(hist): dict"]),
    (5.5, 2.5, 4.5, 2.2, "QuizUtils",
     [],
     ["generate_quiz_structured(topic, n, diff): list"]),
    (10.5, 7.5, 4.5, 1.8, "NotesUtils",
     [],
     ["generate_notes(text, fmt, path): str"]),
    (10.5, 5.0, 4.5, 2.2, "RoadmapUtils",
     [],
     ["generate_roadmap_structured(goal, wks, hrs, path): list"]),
    (10.5, 2.5, 4.5, 2.2, "StorageUtils",
     [],
     ["load_session_data(): dict", "save_study_plan(id, plan)", "update_progress(id, prog)"]),
]

for cx, cy, cw, ch, cname, attrs, methods in classes:
    # Class box
    rect = FancyBboxPatch((cx, cy), cw, ch, boxstyle="round,pad=0.05",
                          facecolor=SURFACE, edgecolor=ACCENT, linewidth=1.5)
    ax.add_patch(rect)
    
    # Title section
    title_h = 0.45
    trect = FancyBboxPatch((cx, cy + ch - title_h), cw, title_h, boxstyle="square,pad=0",
                           facecolor=SURFACE2, edgecolor='none')
    ax.add_patch(trect)
    ax.text(cx + cw/2, cy + ch - title_h/2, cname, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=ACCENT)
    
    # Divider
    ax.plot([cx, cx+cw], [cy + ch - title_h, cy + ch - title_h], color=ACCENT, lw=0.8)
    
    y_offset = cy + ch - title_h - 0.02
    for attr in attrs:
        y_offset -= 0.28
        ax.text(cx + 0.15, y_offset, f"  {attr}", va='center', fontsize=6.5, color=MUTED)
    
    if attrs and methods:
        ax.plot([cx, cx+cw], [y_offset - 0.08, y_offset - 0.08], color=BORDER, lw=0.6)
        y_offset -= 0.15
    
    for m in methods:
        y_offset -= 0.27
        ax.text(cx + 0.15, y_offset, f"+ {m}", va='center', fontsize=6.5, color=TEXT)

# Dependency arrows from App to utils
for tx, ty in [(7.75, 9.3), (7.75, 7.1), (7.75, 4.6), (12.75, 9.3), (12.75, 7.1), (12.75, 4.6)]:
    ax.annotate("", xy=(tx, ty), xytext=(3.0, 7.5),
                arrowprops=dict(arrowstyle="->", color=BORDER, lw=1, connectionstyle="arc3,rad=0.1"))

save(fig, "uml_class_diagram")


# ─── 3. SEQUENCE DIAGRAM — AI Tutor Flow ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(7, 9.6, "Sequence Diagram — AI Tutor Interaction", ha='center', fontsize=14,
        fontweight='bold', color=TEXT)

# Lifelines
lifelines = [
    (1.5, "User"),
    (4.5, "Streamlit UI"),
    (7.5, "SentimentUtils"),
    (10.5, "AIUtils"),
    (13.0, "Groq API")
]

for lx, lname in lifelines:
    ax.text(lx, 9.1, lname, ha='center', va='center', fontsize=9,
            fontweight='bold', color=TEXT,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=SURFACE2, edgecolor=ACCENT, linewidth=1.2))
    ax.plot([lx, lx], [0.2, 8.8], color=BORDER, lw=1, linestyle='--')

# Messages (y, x_from, x_to, label, color)
messages = [
    (8.3, 1.5, 4.5, "Type question + click Send", ACCENT),
    (7.7, 4.5, 7.5, "analyze_text_sentiment(input)", ACCENT2),
    (7.1, 7.5, 4.5, "sentiment: 'Positive'", ACCENT2),
    (6.5, 4.5, 4.5, "append to chat_history", MUTED),
    (5.9, 4.5, 10.5, "generate_ai_response(messages, system)", ACCENT),
    (5.3, 10.5, 13.0, "POST /v1/messages", ACCENT3),
    (4.7, 13.0, 10.5, "AI response text", ACCENT3),
    (4.1, 10.5, 4.5, "return response string", ACCENT),
    (3.5, 4.5, 7.5, "analyze_text_sentiment(response)", ACCENT2),
    (2.9, 7.5, 4.5, "sentiment: 'Positive'", ACCENT2),
    (2.3, 4.5, 4.5, "append AI msg + rerun()", MUTED),
    (1.7, 4.5, 1.5, "Render updated chat", ACCENT),
]

for my, mx1, mx2, label, color in messages:
    if mx1 == mx2:
        # Self-loop
        ax.annotate("", xy=(mx1 + 0.3, my - 0.3), xytext=(mx1, my),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.2,
                                   connectionstyle="arc3,rad=-0.4"))
        ax.text(mx1 + 0.5, my - 0.15, label, fontsize=7, color=color)
    else:
        ax.annotate("", xy=(mx2, my), xytext=(mx1, my),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.2))
        mid = (mx1 + mx2) / 2
        ax.text(mid, my + 0.12, label, ha='center', fontsize=7.5, color=color)

save(fig, "sequence_diagram_tutor")


# ─── 4. SEQUENCE DIAGRAM — Quiz Flow ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 12)
ax.set_ylim(0, 9)
ax.axis('off')

ax.text(6, 8.6, "Sequence Diagram — Quiz Generation & Submission", ha='center', fontsize=13,
        fontweight='bold', color=TEXT)

lifelines2 = [(1.5, "User"), (4.0, "Streamlit UI"), (7.0, "QuizUtils"), (10.5, "Groq API")]
for lx, lname in lifelines2:
    ax.text(lx, 8.2, lname, ha='center', va='center', fontsize=9, fontweight='bold', color=TEXT,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=SURFACE2, edgecolor=ACCENT, linewidth=1.2))
    ax.plot([lx, lx], [0.2, 7.9], color=BORDER, lw=1, linestyle='--')

msgs2 = [
    (7.5, 1.5, 4.0, "Enter topic, select difficulty, click Generate", ACCENT),
    (6.8, 4.0, 7.0, "generate_quiz_structured(topic, n, diff)", ACCENT),
    (6.1, 7.0, 10.5, "POST /v1/messages (structured JSON prompt)", ACCENT3),
    (5.4, 10.5, 7.0, "JSON array of questions", ACCENT3),
    (4.7, 7.0, 7.0, "Parse & validate JSON", MUTED),
    (4.0, 7.0, 4.0, "return list[dict]", ACCENT2),
    (3.3, 4.0, 4.0, "Store in quiz_state, render options", MUTED),
    (2.6, 1.5, 4.0, "Select answers for each question", ACCENT),
    (1.9, 1.5, 4.0, "Click 'Reveal Answers'", ACCENT),
    (1.2, 4.0, 4.0, "Score, log to quiz_sessions_log + chat_history", MUTED),
]

for my, mx1, mx2, label, color in msgs2:
    if mx1 == mx2:
        ax.annotate("", xy=(mx1 + 0.4, my - 0.35), xytext=(mx1, my),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.2, connectionstyle="arc3,rad=-0.4"))
        ax.text(mx1 + 0.6, my - 0.15, label, fontsize=7.5, color=color)
    else:
        ax.annotate("", xy=(mx2, my), xytext=(mx1, my),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.2))
        mid = (mx1 + mx2) / 2
        ax.text(mid, my + 0.12, label, ha='center', fontsize=7.5, color=color)

save(fig, "sequence_diagram_quiz")


# ─── 5. USE CASE DIAGRAM ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(7, 9.6, "Use Case Diagram — IntelliLearn AI", ha='center', fontsize=14,
        fontweight='bold', color=TEXT)

# System boundary
sys_rect = FancyBboxPatch((1.5, 0.5), 9, 8.8, boxstyle="round,pad=0.1",
                           facecolor='none', edgecolor=ACCENT, linewidth=1.5, linestyle='--')
ax.add_patch(sys_rect)
ax.text(6, 9.15, "IntelliLearn AI System", ha='center', fontsize=9, color=ACCENT)

# Actor (Student)
ax.plot([0.7], [5.0], 'o', color=ACCENT2, markersize=14)
ax.plot([0.5, 0.9], [4.6, 4.6], color=ACCENT2, lw=2)
ax.plot([0.7, 0.5], [4.6, 4.0], color=ACCENT2, lw=2)
ax.plot([0.7, 0.9], [4.6, 4.0], color=ACCENT2, lw=2)
ax.text(0.7, 3.6, "Student", ha='center', fontsize=9, color=ACCENT2, fontweight='bold')

# Actor (Groq AI)
ax.plot([13.3], [5.0], 'o', color=ACCENT3, markersize=14)
ax.plot([13.1, 13.5], [4.6, 4.6], color=ACCENT3, lw=2)
ax.plot([13.3, 13.1], [4.6, 4.0], color=ACCENT3, lw=2)
ax.plot([13.3, 13.5], [4.6, 4.0], color=ACCENT3, lw=2)
ax.text(13.3, 3.6, "Groq AI API", ha='center', fontsize=9, color=ACCENT3, fontweight='bold')

# Use cases
use_cases = [
    (6, 8.3, "Select Learning Path"),
    (6, 7.2, "Ask AI Tutor"),
    (6, 6.1, "Generate Quiz"),
    (6, 5.0, "Answer Quiz & Get Score"),
    (6, 3.9, "Generate Notes"),
    (6, 2.8, "Create Study Roadmap"),
    (6, 1.7, "Track Roadmap Progress"),
    (6, 0.8, "View Dashboard & Sentiment"),
]

for ux, uy, ulabel in use_cases:
    ellipse = mpatches.Ellipse((ux, uy), 4.0, 0.6, facecolor=SURFACE2, edgecolor=ACCENT, linewidth=1.2)
    ax.add_patch(ellipse)
    ax.text(ux, uy, ulabel, ha='center', va='center', fontsize=8.5, color=TEXT)
    # Line from student
    ax.plot([1.0, ux - 2.0], [5.0, uy], color=BORDER, lw=0.8)
    # Line to Groq for AI-heavy tasks
    if ulabel in ["Ask AI Tutor", "Generate Quiz", "Generate Notes", "Create Study Roadmap"]:
        ax.plot([ux + 2.0, 12.9], [uy, 5.0], color=BORDER, lw=0.8, linestyle=':')

save(fig, "use_case_diagram")


# ─── 6. ACTIVITY DIAGRAM — Full App Flow ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 16))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis('off')

ax.text(5, 15.6, "Activity Diagram — IntelliLearn AI", ha='center', fontsize=14,
        fontweight='bold', color=TEXT)

def activity_box(ax, x, y, w, h, text, color=SURFACE2, border=ACCENT, fontsize=9):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor=border, linewidth=1.2)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, color=TEXT, wrap=True)

def decision_diamond(ax, x, y, size, text):
    diamond = plt.Polygon([[x, y+size], [x+size*1.5, y], [x, y-size], [x-size*1.5, y]],
                          facecolor=SURFACE2, edgecolor=ACCENT3, linewidth=1.2)
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center', fontsize=8, color=ACCENT3)

def arrow(ax, x1, y1, x2, y2, label="", color=BORDER):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.2))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.15, my, label, fontsize=7.5, color=MUTED)

# Start
ax.plot([5], [15.1], 'o', color=ACCENT, markersize=12)
arrow(ax, 5, 15.0, 5, 14.55)

activity_box(ax, 5, 14.3, 4, 0.45, "Open IntelliLearn AI")
arrow(ax, 5, 14.05, 5, 13.6)

activity_box(ax, 5, 13.35, 4, 0.45, "Home Page Loaded")
arrow(ax, 5, 13.1, 5, 12.7)

decision_diamond(ax, 5, 12.3, 0.35, "Select\nPath?")
arrow(ax, 5, 11.95, 5, 11.55, "Yes")
ax.text(5.5, 12.3, "No", fontsize=7.5, color=MUTED, va='center')

activity_box(ax, 5, 11.3, 4, 0.45, "Set Learning Path (preset or custom)")
arrow(ax, 5, 11.05, 5, 10.6)

activity_box(ax, 5, 10.35, 5, 0.45, "Choose Feature (Tutor / Quiz / Notes / Roadmap)")
arrow(ax, 5, 10.1, 5, 9.7)

decision_diamond(ax, 5, 9.3, 0.35, "Which\nfeature?")

# Branches
for bx, by, blabel, btext in [
    (1.8, 8.0, "AI Tutor", "Type question\n→ Sentiment check\n→ Groq API call\n→ Show answer"),
    (3.8, 8.0, "Quiz", "Set topic/diff\n→ Generate quiz\n→ Answer options\n→ Reveal & score"),
    (6.2, 8.0, "Notes", "Paste content\n→ Choose format\n→ Groq generates\n→ Show notes"),
    (8.5, 8.0, "Roadmap", "Set goal/weeks\n→ Groq generates\n→ Track milestones"),
]:
    ax.annotate("", xy=(bx, 8.4), xytext=(5, 8.95),
                arrowprops=dict(arrowstyle="->", color=BORDER, lw=1, connectionstyle="arc3,rad=0"))
    ax.text(bx, 8.2, blabel, ha='center', fontsize=7.5, color=ACCENT, fontweight='bold')
    rect = FancyBboxPatch((bx-1.1, 6.9), 2.2, 1.1, boxstyle="round,pad=0.05",
                          facecolor=SURFACE2, edgecolor=BORDER, linewidth=1)
    ax.add_patch(rect)
    ax.text(bx, 7.45, btext, ha='center', va='center', fontsize=6.5, color=TEXT)

# Merge back
for bx2 in [1.8, 3.8, 6.2, 8.5]:
    ax.annotate("", xy=(5, 6.4), xytext=(bx2, 6.9),
                arrowprops=dict(arrowstyle="->", color=BORDER, lw=1, connectionstyle="arc3,rad=0"))

activity_box(ax, 5, 6.1, 5, 0.5, "Data logged to session state\n(chat history, quiz log, progress)")
arrow(ax, 5, 5.85, 5, 5.45)

activity_box(ax, 5, 5.2, 4.5, 0.45, "Dashboard updated with real analytics")
arrow(ax, 5, 4.95, 5, 4.55)

decision_diamond(ax, 5, 4.15, 0.35, "Continue?")
arrow(ax, 5, 3.8, 5, 10.35, "Yes")
arrow(ax, 5, 3.8, 5, 3.4, "No")
ax.text(5.2, 3.85, "No", fontsize=7.5, color=MUTED)
ax.text(4.1, 4.15, "Yes", fontsize=7.5, color=MUTED)

activity_box(ax, 5, 3.15, 3.5, 0.45, "End Session")
# End marker
ax.plot([5], [2.75], 'o', color=ACCENT, markersize=12)
ax.plot([5], [2.75], 'o', color=BG, markersize=7)
arrow(ax, 5, 2.9, 5, 2.82)

save(fig, "activity_diagram")


# ─── 7. COMPONENT DIAGRAM ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

ax.text(7, 7.6, "Component Diagram — IntelliLearn AI", ha='center', fontsize=14,
        fontweight='bold', color=TEXT)

components = [
    (0.3, 3.5, 2.5, 3.5, "Frontend", ACCENT, [
        "app.py\n(Streamlit UI)", "CSS Styling", "Session State"
    ]),
    (3.2, 4.5, 2.5, 2.5, "Core Utils", ACCENT2, [
        "ai_utils.py", "sentiment_utils.py"
    ]),
    (3.2, 1.5, 2.5, 2.5, "Feature Utils", ACCENT2, [
        "quiz_utils.py", "notes_utils.py", "roadmap_utils.py"
    ]),
    (6.1, 3.5, 2.5, 3.5, "Data Layer", "#6c63ff", [
        "session_state", "chat_history", "study_plans", "quiz_logs"
    ]),
    (9.0, 4.5, 2.5, 2.5, "External AI", ACCENT3, [
        "Groq API", "LLaMA 3.1 8B"
    ]),
    (9.0, 1.5, 2.5, 2.5, "NLP", ACCENT3, [
        "VADER Sentiment", "Text Analyzer"
    ]),
    (12.0, 3.5, 1.7, 3.5, "Config", MUTED, [
        ".env", "API Keys", "Model Config"
    ]),
]

for cx, cy, cw, ch, cname, color, items in components:
    rect = FancyBboxPatch((cx, cy), cw, ch, boxstyle="round,pad=0.08",
                          facecolor=SURFACE, edgecolor=color, linewidth=1.5)
    ax.add_patch(rect)
    trect = FancyBboxPatch((cx, cy + ch - 0.5), cw, 0.5, boxstyle="square,pad=0",
                           facecolor=SURFACE2, edgecolor='none')
    ax.add_patch(trect)
    ax.text(cx + cw/2, cy + ch - 0.25, cname, ha='center', va='center',
            fontsize=9, fontweight='bold', color=color)
    ax.plot([cx, cx+cw], [cy + ch - 0.5, cy + ch - 0.5], color=color, lw=0.8)
    
    y_item = cy + ch - 0.8
    for item in items:
        y_item -= 0.55
        ax.text(cx + cw/2, y_item, f"• {item}", ha='center', va='center', fontsize=7.5, color=MUTED)

# Connection lines
connections = [
    (2.8, 5.25, 3.2, 5.7),   # Frontend -> Core Utils
    (2.8, 4.5, 3.2, 3.0),    # Frontend -> Feature Utils
    (2.8, 5.25, 6.1, 5.25),  # Frontend -> Data
    (5.7, 5.7, 6.1, 5.7),    # Core Utils -> Data
    (5.7, 3.0, 6.1, 4.0),    # Feature Utils -> Data
    (5.7, 5.5, 9.0, 5.5),    # Core Utils -> Groq
    (5.7, 2.5, 9.0, 2.5),    # Feature Utils -> NLP
    (5.7, 5.0, 9.0, 4.8),    # Core Utils -> Groq
    (11.5, 5.25, 12.0, 5.25), # Groq -> Config
]
for x1, y1, x2, y2 in connections:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=BORDER, lw=1.0))

save(fig, "component_diagram")

print("\n✅ All diagrams generated successfully!")
print(f"   Saved to: {OUT}/")
