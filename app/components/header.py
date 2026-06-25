import streamlit as st


def render_header():
    """Render the Query AI application header."""

    st.title("🧠 Query AI")

    st.caption(
        "AI-powered Document, Text & Code Intelligence"
    )

    st.markdown(
        """
Chat with documents, analyze text, review source code, and gain intelligent
insights from a unified AI-powered workspace.
"""
    )

    st.divider()