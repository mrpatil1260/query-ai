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
from app.services.text_analysis_service import analyze_text
from app.services.code_analysis_service import analyze_code
from app.components.header import render_header
from app.components.sidebar import render_sidebar
from app.components.chat import render_chat_history
from app.components.uploader import render_uploader
from app.components.actions import render_actions
from app.components.text_workspace import render_text_workspace
from app.components.code_workspace import render_code_workspace
from app.components.footer import render_footer
# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Query AI",
    page_icon="🧠",
    layout="wide",
)
# -------------------------
# Session State
# -------------------------
if "indexed_file" not in st.session_state:
    st.session_state.indexed_file = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_count" not in st.session_state:
    st.session_state.document_count = 0
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

render_header()



if (
    st.session_state.get("document_count", 0) == 0
    and not st.session_state.get("chat_history")
):
    st.caption(
        "🚀 Upload documents, analyze text, or review source code to get started."
    )

# -------------------------
# Sidebar
# -------------------------
if render_sidebar():
    st.session_state.chat_history = []
    st.rerun()

actions = render_actions()

documents_tab, text_tab, code_tab = st.tabs(
    [
        "📄 Documents",
        "📝 Text Intelligence",
        "💻 Code Intelligence",
    ]
)

with documents_tab:
    # -------------------------
    # Upload PDF
    # -------------------------
    uploaded_files = render_uploader()

    if uploaded_files:
        try:
            total_chunks = 0
            processed_documents = 0

            with st.spinner("📄 Processing PDF and building vector database..."):

                reset_collection()

                for uploaded_file in uploaded_files:
                    os.makedirs("data/uploads", exist_ok=True)

                    unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"

                    upload_path = os.path.join(
                        "data",
                        "uploads",
                        unique_filename,
                    )

                    with open(upload_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

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
                        source_name=uploaded_file.name,
                    )

                    processed_documents += 1
                    total_chunks += len(chunks)

                st.session_state.document_count = processed_documents
                st.session_state.chunk_count = total_chunks
                st.session_state.indexed_file = "MULTI_PDF_SESSION"
                st.session_state.chat_history = []

            st.success(f"✅ Indexed {processed_documents} document(s) with {total_chunks} chunks successfully!")

            if actions["summarize"]:

                with st.spinner("📝 Generating summary..."):

                    query_embedding = embed_query(
                        "Give me a comprehensive summary of all uploaded documents."
                    )

                    results = search(
                        query_embedding=query_embedding,
                        n_results=10,
                    )

                    docs = results.get("documents", [])

                    if docs and docs[0]:
                        context = "\n\n".join(docs[0])

                        summary = ask_llm(
                            context=context,
                            question=(
                                "Provide a concise but comprehensive summary of all uploaded documents."
                            ),
                        )

                        st.subheader("📝 AI Summary")
                        st.write(summary)
                    else:
                        st.warning("No documents available to summarize.")

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
                    metadatas = results.get("metadatas", [])

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
                                "metadata": (
                                    metadatas[0]
                                    if metadatas
                                    else []
                                ),
                            }
                        )

            # -------------------------
            # Chat History
            # -------------------------
            render_chat_history(st.session_state.chat_history)

        except Exception as e:
            st.error(
                f"❌ An unexpected error occurred:\n\n{e}"
            )

with text_tab:
    text_input, text_action = render_text_workspace()
    if text_input and st.button("🚀 Run Text Analysis", key="text_analysis_button"):
        response = analyze_text(
            text=text_input,
            action=text_action,
        )
        st.subheader("🤖 Result")
        st.write(response)

with code_tab:
    code, language, code_action = render_code_workspace()
    if code and st.button("🚀 Analyze Code", key="code_analysis_button"):
        response = analyze_code(
            code=code,
            language=language,
            action=code_action,
        )
        st.subheader("🤖 Analysis")
        st.write(response)

render_footer()