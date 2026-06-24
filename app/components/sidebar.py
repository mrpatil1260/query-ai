import streamlit as st


def render_sidebar():
    st.sidebar.title("🧠 Query AI")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Features")

    st.sidebar.markdown(
        """
- 📄 Multi-document chat
- 📝 Text intelligence
- 💻 Code analysis
- 🎯 Career Copilot
- 📊 Skill gap analysis
- 🔑 ATS recommendations
- 🎤 Interview preparation
"""
    )

    st.sidebar.markdown("---")

    clear = st.sidebar.button("🗑️ Clear Chat")

    st.sidebar.caption("Version 1.0")

    return clear