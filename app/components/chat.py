import streamlit as st


def render_chat_history(chat_history):
    """Render the conversation history with optional source references."""

    if not chat_history:
        st.info(
            "👋 Welcome! Upload a document, paste text, paste code, or ask a question to get started."
        )
        return

    for chat in chat_history:
        question = chat.get("question", "")
        answer = chat.get("answer") or "No response generated."

        with st.chat_message("user", avatar="👤"):
            st.markdown(question)

        with st.chat_message("assistant", avatar="🧠"):
            st.markdown(answer)

            sources = chat.get("sources", [])
            metadata = chat.get("metadata", [])

            if sources:
                st.caption("📚 Sources")
                with st.expander("📚 View Sources"):

                    for i, source in enumerate(sources):

                        meta = metadata[i] if i < len(metadata) and isinstance(metadata[i], dict) else {}
                        source_name = meta.get("source", "Unknown Document")

                        st.markdown(
                            f"**📄 {source_name} • Reference {i + 1}**"
                        )

                        st.write(source)
                        st.divider()
        st.markdown("")