import streamlit as st

from utils.ai_utils import generate_ai_response
from utils.sentiment_utils import analyze_sentiment
from utils.quiz_utils import generate_quiz
from utils.notes_utils import generate_notes
from utils.roadmap_utils import generate_roadmap

from components.dashboard import render_dashboard

st.set_page_config(
    page_title="IntelliLearn AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 IntelliLearn AI")
st.caption("Personalized AI-Powered Learning Assistant")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "AI Tutor",
        "Quiz Generator",
        "Notes Generator",
        "Sentiment Analyzer",
        "Study Roadmap",
        "Dashboard"
    ]
)

# HOME
if menu == "Home":

    st.header("Welcome to IntelliLearn AI")

    st.write("""
    IntelliLearn AI helps students:
    - learn faster,
    - generate study notes,
    - create quizzes,
    - analyze learning confidence,
    - and build personalized study roadmaps.
    """)

# AI TUTOR
elif menu == "AI Tutor":

    st.header("AI Tutor Assistant")

    topic = st.text_input(
        "Enter a topic"
    )

    if st.button("Generate Explanation"):

        prompt = f"""
        Explain the following topic to a beginner:

        {topic}

        Include:
        - simple explanation
        - examples
        - real-world analogy
        """

        response = generate_ai_response(prompt)

        st.write(response)

# QUIZ GENERATOR
elif menu == "Quiz Generator":

    st.header("Smart Quiz Generator")

    topic = st.text_input(
        "Enter quiz topic"
    )

    if st.button("Generate Quiz"):

        quiz = generate_quiz(topic)

        st.write(quiz)

# NOTES GENERATOR
elif menu == "Notes Generator":

    st.header("AI Notes Generator")

    notes_input = st.text_area(
        "Paste your study content"
    )

    if st.button("Generate Notes"):

        notes = generate_notes(notes_input)

        st.write(notes)

# SENTIMENT ANALYZER
elif menu == "Sentiment Analyzer":

    st.header("Learning Sentiment Analyzer")

    user_text = st.text_area(
        "Describe your learning experience"
    )

    if st.button("Analyze Sentiment"):

        result = analyze_sentiment(user_text)

        st.write(f"Sentiment: {result['sentiment']}")

        st.json(result["scores"])

# STUDY ROADMAP
elif menu == "Study Roadmap":

    st.header("Personalized Study Roadmap")

    goal = st.text_input(
        "Enter your learning goal"
    )

    if st.button("Generate Roadmap"):

        roadmap = generate_roadmap(goal)

        st.write(roadmap)

# DASHBOARD
elif menu == "Dashboard":

    render_dashboard()