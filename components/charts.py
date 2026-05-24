import plotly.express as px
import pandas as pd


def create_progress_chart():

    data = pd.DataFrame({
        "Topic": [
            "Python",
            "Machine Learning",
            "NLP",
            "Data Science",
            "AI Fundamentals"
        ],

        "Progress": [
            80,
            60,
            45,
            70,
            90
        ]
    })

    fig = px.bar(
        data,
        x="Topic",
        y="Progress",
        title="Learning Progress"
    )

    return fig