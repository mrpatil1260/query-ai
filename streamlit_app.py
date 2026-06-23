import os
import uuid
import streamlit as st

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.embedding_service import embed_texts, embed_query
from app.services.chroma_service import (
    add_documents,
    search,
    reset_collection,
)
from app.services.llm_service import ask_llm

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI Knowledge Assistant")
st.caption("Upload a PDF and ask questions using AI-powered Retrieval-Augmented Generation (RAG).")

# -------------------------
# Sidebar
# -------------------------
st.sidebar.title("⚙️ Controls")

# -------------------------
# Session State
# -------------------------
if "indexed_file" not in st.session_state:
    st.session_state.indexed_file = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# -------------------------
# Upload PDF
# -------------------------
uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"],
)

if uploaded_file is not None:
    try:
        os.makedirs("data/uploads", exist_ok=True)

        unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"

        upload_path = os.path.join(
            "data",
            "uploads",
            unique_filename,
        )

        with open(upload_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ PDF uploaded successfully!")

        # Only process once for each uploaded file
        if st.session_state.indexed_file != uploaded_file.name:

            with st.spinner("📄 Processing PDF and building vector database..."):

                reset_collection()

                text = extract_text_from_pdf(upload_path)

                if not text or not text.strip():
                    st.error("❌ No readable text found in the uploaded PDF.")
                    st.stop()

                chunks = chunk_text(text)

                if not chunks:
                    st.error("❌ Failed to generate text chunks.")
                    st.stop()

                embeddings = embed_texts(chunks)

                ids = [
                    f"chunk_{i}"
                    for i in range(len(chunks))
                ]

                add_documents(
                    ids=ids,
                    texts=chunks,
                    embeddings=embeddings,
                )

                st.session_state.indexed_file = uploaded_file.name
                st.session_state.chat_history = []

            st.success(f"✅ Indexed {len(chunks)} chunks successfully!")

        st.divider()

        question = st.text_input(
            "💬 Ask a question about the uploaded PDF"
        )

        if question:

            with st.spinner("🤖 Thinking..."):

                query_embedding = embed_query(question)

                results = search(
                    query_embedding=query_embedding,
                    n_results=5,
                )

                documents = results.get("documents", [])

                if (
                    not documents
                    or len(documents) == 0
                    or len(documents[0]) == 0
                ):
                    st.warning(
                        "No relevant information found."
                    )

                else:

                    context = "\n\n".join(documents[0])

                    answer = ask_llm(
                        context=context,
                        question=question,
                    )

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer,
                            "sources": documents[0],
                        }
                    )

        # -------------------------
        # Chat History
        # -------------------------
        if st.session_state.chat_history:

            st.divider()
            st.subheader("💬 Conversation")

            for idx, chat in enumerate(
                st.session_state.chat_history,
                start=1,
            ):

                st.markdown(f"### 🙋 Question {idx}")
                st.write(chat["question"])

                st.markdown(f"### 🤖 Answer {idx}")
                st.write(chat["answer"])

                with st.expander("📚 View Source Chunks"):
                    for i, source in enumerate(
                        chat.get("sources", []),
                        start=1,
                    ):
                        st.markdown(f"**Chunk {i}**")
                        st.write(source)

    except Exception as e:
        st.error(
            f"❌ An unexpected error occurred:\n\n{e}"
        )