import streamlit as st


def render_chat_history(chat_history):
    """Render the conversation with source document names."""

    if not chat_history:
        st.info(
            "👋 Upload one or more PDFs and ask your first question."
        )
        return

    st.subheader("💬 Conversation")

    for chat in chat_history:

        with st.chat_message("user"):
            st.markdown(chat["question"])

        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

            sources = chat.get("sources", [])
            metadata = chat.get("metadata", [])

            if sources:
                with st.expander("📚 Sources Used"):

                    for i, source in enumerate(sources):

                        source_name = "Unknown Document"

                        if i < len(metadata):
                            source_name = metadata[i].get(
                                "source",
                                "Unknown Document",
                            )

                        st.markdown(
                            f"### 📄 {source_name}"
                        )

                        st.caption(
                            f"Chunk {i + 1}"
                        )

                        st.write(source)