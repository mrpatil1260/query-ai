import streamlit as st


def render_actions():
    """
    Render AI action buttons.
    """

    st.sidebar.markdown("## 🧠 AI Tools")

    summarize = st.sidebar.button(
        "📝 Generate Summary",
        use_container_width=True,
    )

    return {
        "summarize": summarize,
    }