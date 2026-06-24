import streamlit as st


def render_stats(documents: int, chunks: int, questions: int):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Documents", documents)

    with col2:
        st.metric("Chunks", chunks)

    with col3:
        st.metric("Questions", questions)