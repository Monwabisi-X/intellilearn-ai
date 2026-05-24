# IntelliLearn AI — Architecture Overview

## System Architecture

![Architecture Diagram](images/architecture_diagram.png)

IntelliLearn AI uses a **four-layer clean architecture** designed for educational AI delivery.

### Why This Architecture?

| Decision | Rationale |
|---|---|
| Streamlit for UI | Rapid prototyping, Python-native, zero frontend build tooling |
| Groq (LLaMA 3.1) | Free tier, extremely fast inference (suitable for real-time chat UX) |
| VADER for sentiment | Lightweight, no API call needed, runs locally |
| Session state storage | Simple, sufficient for prototype; easily swappable for a DB |
| JSON-structured AI outputs | Enables reliable programmatic consumption of AI responses |

## Data Flow

```
User Input
    │
    ▼
Streamlit UI (app.py)
    │
    ├── Sentiment check (VADER — local, instant)
    │
    ├── Feature Utils (quiz / notes / roadmap)
    │       │
    │       └── AIUtils → Groq API → LLaMA 3.1 → Response
    │
    ├── Session State Update
    │       (chat_history, quiz_sessions_log, study_plans)
    │
    └── UI Re-render (st.rerun())
```

## Key Architectural Decisions

### 1. Multi-turn Conversation (AI Tutor)
Rather than sending only the current message to the API, the last 10 messages are included in each request. This enables the AI to reference earlier parts of the conversation, making explanations contextually coherent.

### 2. Sentiment as a Cross-Cutting Concern
Sentiment analysis runs on every user message and quiz result. This data is stored alongside chat history, making it available to the Dashboard without a separate "Sentiment tab". The user never has to consciously think about sentiment — it is derived passively from normal usage.

### 3. Learning Path as Global Context
The selected learning path is stored in `session_state` and injected into the system prompt of the AI Tutor, the notes generation prompt, and the roadmap generation prompt. This creates a cohesive learning experience where all features feel connected to the same goal.

### 4. Study Plan Persistence
Study plan progress is stored as a nested dictionary in `session_state`: `{plan_id: {week_idx: {milestone_idx: bool}}}`. This allows granular per-milestone tracking and overall progress computation without any database. Future versions can persist this to disk or a cloud store.
