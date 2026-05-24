# 🎓 IntelliLearn AI

> **An end-to-end AI-powered learning platform** — Week 4 Capstone | CAPACITI × Clickatell AI Bootcamp 2026

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.1-orange)](https://groq.com)

---

## 📌 Project Overview

IntelliLearn AI is a personalised AI learning companion for the **Education** industry. It integrates multiple AI capabilities into a single, cohesive platform where every feature connects to a unified learning experience.

**Industry:** Education / EdTech  
**AI Model:** LLaMA 3.1 8B via Groq API  
**Sentiment:** VADER (real-time, conversation-derived)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 **Home** | Feature tiles, real-time sentiment badge, learning path selector |
| 🤖 **AI Tutor** | Multi-turn chat with learning path context; per-message sentiment tracking |
| ❓ **Quiz Generator** | Interactive MCQ quizzes — answer first, reveal after; auto-logs scores |
| 📝 **Notes Generator** | 4 output formats from any pasted content |
| 🗺️ **Study Roadmap** | AI week-by-week plans with persistent milestone tracking |
| 📊 **Dashboard** | Real analytics from actual usage — sentiment, quiz scores, progress |

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your API key
cp .env.example .env
# Edit .env → add your GROQ_API_KEY (free at console.groq.com)

# 3. Run
streamlit run app.py
```

---

## 📂 Project Structure

```
intellilearn-ai/
├── app.py                    # Main app — UI, navigation, all page logic
├── requirements.txt
├── .env.example
├── utils/
│   ├── ai_utils.py           # Groq API wrapper
│   ├── sentiment_utils.py    # VADER sentiment (per-message + history)
│   ├── quiz_utils.py         # Structured JSON quiz generation
│   ├── notes_utils.py        # Multi-format notes generation
│   ├── roadmap_utils.py      # Week-by-week roadmap generation
│   └── storage_utils.py      # Session state persistence layer
└── docs/
    ├── technical_documentation.md
    ├── prompt_case_study.md
    ├── architecture.md
    └── images/
        ├── architecture_diagram.png
        ├── uml_class_diagram.png
        ├── sequence_diagram_tutor.png
        ├── sequence_diagram_quiz.png
        ├── use_case_diagram.png
        ├── activity_diagram.png
        └── component_diagram.png
```

---

## 🧠 AI Architecture

```
User Message
     │
     ├─► VADER Sentiment (local, instant)
     │
     └─► Groq API (LLaMA 3.1 8B)
              │
              ├── AI Tutor: multi-turn conversation (last 10 msgs)
              ├── Quiz: structured JSON prompt → 5-10 MCQs
              ├── Notes: format-specific prompt → markdown
              └── Roadmap: JSON schema prompt → week objects
```

---

## 📊 Responsible AI

- Quiz answers are **never shown automatically** — students must click "Reveal Answers"
- All sentiment data is derived from user's own messages (no third-party profiling)
- No user data is stored beyond the current session
- AI-generated content is clearly labelled throughout the UI

---

## 📄 Documentation

See [`docs/technical_documentation.md`](docs/technical_documentation.md) for:
- Full architecture diagram
- UML class diagram  
- Sequence diagrams (AI Tutor + Quiz)
- Use case diagram
- Activity diagram
- Component diagram
- Prompt engineering case study
- Responsible AI considerations

---

## 🔑 Getting a Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Create an API key
4. Paste it into your `.env` file

---

*Built with ❤️ for the CAPACITI × Clickatell AI Bootcamp — Week 4 Capstone*
