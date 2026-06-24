import streamlit as st


def render_header():
    """Render the application hero header."""

    st.markdown(
        """
        <div style="
            padding: 1.5rem 1.75rem;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            background-color: #F8FAFC;
            margin-bottom: 1rem;
        ">
            <h1 style="margin:0;color:#111827;">
                🧠 Query AI
            </h1>

            <p style="
                margin-top:0.4rem;
                margin-bottom:0.8rem;
                font-size:1.1rem;
                color:#374151;
            ">
                AI-powered Document, Code & Career Intelligence
            </p>

            <p style="
                margin:0;
                color:#6B7280;
                line-height:1.6;
            ">
                Chat with documents, summarize text, analyze code,
                compare resumes with job descriptions, identify skill gaps,
                and prepare for interviews from one unified workspace.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )