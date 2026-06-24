import streamlit as st


def render_footer():
    """Render a simple application footer."""

    st.divider()

    st.caption(
        "🧠 Query AI • Built with Python, Streamlit, ChromaDB, Sentence Transformers & LLMs"
    )