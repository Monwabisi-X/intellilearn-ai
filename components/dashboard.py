import streamlit as st
from components.charts import create_progress_chart


def render_dashboard():

    st.subheader("Learning Analytics Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Topics Completed",
        "12"
    )

    col2.metric(
        "Average Quiz Score",
        "84%"
    )

    col3.metric(
        "Study Hours",
        "42"
    )

    fig = create_progress_chart()

    st.plotly_chart(
        fig,
        use_container_width=True
    )