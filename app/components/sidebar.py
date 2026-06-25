import streamlit as st


def render_sidebar(conversations=None):
    st.sidebar.title("🧠 Query AI")
    st.sidebar.caption("Your AI workspace")

    new_chat = st.sidebar.button(
        "✨ New Chat",
        use_container_width=True,
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("💬 Chats")
    if conversations and len(conversations) > 0:
        for entry in conversations:
            title = entry.get("title", "New Chat").strip()
            if not title:
                continue
            if len(title) > 40:
                truncated = title[:40] + "..."
            else:
                truncated = title
            if st.sidebar.button(f"💬 {truncated}", use_container_width=True, key=f"chat_{entry.get('id','')}"):
                st.session_state.current_chat_id = entry.get('id')
    else:
        st.sidebar.caption("No messages yet")

    st.sidebar.markdown("---")
    st.sidebar.caption("Query AI v1.0")

    return new_chat