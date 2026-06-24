import streamlit as st


def render_stats(documents: int, chunks: int, questions: int):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(

            label="📄 Documents",

            value=documents,

            help="Number of uploaded documents",

        )

    with col2:
        st.metric(

            label="✂️ Chunks",

            value=chunks,

            help="Text chunks indexed for semantic search",

        )

    with col3:
        st.metric(

            label="💬 Conversations",

            value=questions,

            help="Questions asked in this session",

        )