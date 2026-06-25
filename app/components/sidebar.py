import streamlit as st


def render_sidebar():
    st.sidebar.title("🧠 Query AI")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Capabilities")

    st.sidebar.markdown(
        """
- 📄 Chat with PDF documents
- 🔍 Semantic document search
- 📝 Text Intelligence
- 💻 Code Intelligence
- 🤖 AI-powered insights
"""
    )

    st.sidebar.markdown("---")

    clear = st.sidebar.button("🗑️ Clear Conversation")

    st.sidebar.caption("Query AI • v1.0")

    return clear