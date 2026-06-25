import os
import uuid
import streamlit as st

from app.services.pdf_service import extract_text_from_file
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
from app.components.sidebar import render_sidebar
from app.components.chat import render_chat_history
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
# Session State Initialization
# -------------------------
if "indexed_file" not in st.session_state:
    st.session_state.indexed_file = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_count" not in st.session_state:
    st.session_state.document_count = 0
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False
if "last_uploaded_files" not in st.session_state:
    st.session_state.last_uploaded_files = []
if "text_analysis_results" not in st.session_state:
    st.session_state.text_analysis_results = None
if "code_analysis_results" not in st.session_state:
    st.session_state.code_analysis_results = None

# New unified active context state
if "active_context_type" not in st.session_state:
    st.session_state.active_context_type = None
if "active_context" not in st.session_state:
    st.session_state.active_context = ""

# ChatGPT-style multi-chat support
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "current_chat_title" not in st.session_state:
    st.session_state.current_chat_title = "New Chat"

# -------------------------
# Title / Header (minimal)
# -------------------------
st.title("Query AI 🧠")
if not st.session_state.chat_history:
    st.info("👋 Welcome! Upload a document, paste text, paste code, or ask me anything to get started.")

# -------------------------
# Sidebar handling
# -------------------------
if render_sidebar(st.session_state.get("conversations", [])):
    st.session_state.chat_history = []
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.current_chat_title = "New Chat"
    st.session_state.documents_processed = False
    st.session_state.document_count = 0
    st.session_state.chunk_count = 0
    st.session_state.indexed_file = None
    st.session_state.last_uploaded_files = []
    st.session_state.active_context_type = None
    st.session_state.active_context = ""
    st.rerun()

# -------------------------
# Render chat history
# -------------------------
render_chat_history(st.session_state.chat_history)

# -------------------------
# Expander: Upload Document
# -------------------------
with st.expander("📎 Upload Document", expanded=True):
    uploaded_files = st.file_uploader(
        label="Upload documents",
        type=["pdf", "docx", "txt", "md", "csv"],
        accept_multiple_files=True,
        help="Upload one or more documents (PDF, DOCX, TXT, Markdown, CSV) to index and query."
    )

    current_uploaded_files = (
        sorted(file.name for file in uploaded_files)
        if uploaded_files
        else []
    )

    if current_uploaded_files != st.session_state.last_uploaded_files:
        st.session_state.last_uploaded_files = current_uploaded_files
        reset_collection()
        st.session_state.indexed_file = None
        st.session_state.documents_processed = False
        st.session_state.chat_history = []
        st.session_state.document_count = 0
        st.session_state.chunk_count = 0
        st.session_state.active_context_type = None
        st.session_state.active_context = ""

    if (
        uploaded_files
        and len(uploaded_files) > 0
        and not st.session_state.documents_processed
    ):
        try:
            total_chunks = 0
            processed_documents = 0
            full_context = ""

            with st.spinner("⚡ Processing your documents..."):

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

                    text = extract_text_from_file(upload_path)

                    if not text or not text.strip():
                        st.error("❌ No readable text found in the uploaded document.")
                        st.stop()

                    full_context += f"\n\n===== {uploaded_file.name} =====\n\n"
                    full_context += text
                    full_context += "\n\n"

                    chunks = chunk_text(text)

                    if not chunks:
                        st.error("❌ Failed to generate text chunks.")
                        st.stop()

                    embeddings = embed_texts(chunks)

                    ids = [f"{uuid.uuid4()}_{i}" for i in range(len(chunks))]

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
                st.session_state.documents_processed = True
                st.session_state.active_context_type = "document"
                st.session_state.active_context = full_context

            st.toast(
                f"✅ Processed {processed_documents} document(s).",
                icon="🎉",
            )

            st.rerun()

        except Exception as e:
            st.error(
                f"❌ An unexpected error occurred:\n\n{e}"
            )

# -------------------------
# Expander: Paste Text
# -------------------------
with st.expander("📝 Paste Text"):
    text_input = st.text_area(
        label="Paste your text here",
        height=200,
        help="Enter the text you want to analyze."
    )
    text_action = st.selectbox(
        label="Select text analysis action",
        options=[
            "Summarize",
            "Sentiment Analysis",
            "Extract Keywords",
            "Answer Questions",
        ],
        help="Choose the type of text analysis to perform."
    )
    if text_input and st.button("🚀 Run Text Analysis", key="text_analysis_button"):
        response = analyze_text(
            text=text_input,
            action=text_action,
        )
        st.session_state.active_context_type = "text"
        st.session_state.active_context = text_input
        if st.session_state.current_chat_title == "New Chat":
            title_candidate = text_action.strip()[:40]
            st.session_state.current_chat_title = title_candidate
            chat_id = st.session_state.current_chat_id or str(uuid.uuid4())
            st.session_state.current_chat_id = chat_id
            if not any(c.get("id") == chat_id for c in st.session_state.conversations):
                st.session_state.conversations.append({"id": chat_id, "title": st.session_state.current_chat_title})
        st.session_state.chat_history.append(
            {
                "question": f"Text analysis: {text_action}",
                "answer": response,
                "sources": [],
                "metadata": [],
            }
        )
        st.rerun()

# -------------------------
# Expander: Paste Code
# -------------------------
with st.expander("💻 Paste Code"):
    language = st.selectbox(
        label="Select programming language",
        options=[
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "Go",
            "Ruby",
            "Other",
        ],
        help="Select the language of the code you are pasting."
    )
    code = st.text_area(
        label="Paste your code here",
        height=200,
        help="Enter the code you want to analyze."
    )
    code_action = st.selectbox(
        label="Select code analysis action",
        options=[
            "Explain Code",
            "Find Bugs",
            "Suggest Improvements",
            "Generate Tests",
        ],
        help="Choose the type of code analysis to perform."
    )
    if code and st.button("🚀 Analyze Code", key="code_analysis_button"):
        response = analyze_code(
            code=code,
            language=language,
            action=code_action,
        )
        st.session_state.active_context_type = "code"
        st.session_state.active_context = code
        if st.session_state.current_chat_title == "New Chat":
            title_candidate = f"{language}: {code_action}".strip()[:40]
            st.session_state.current_chat_title = title_candidate
            chat_id = st.session_state.current_chat_id or str(uuid.uuid4())
            st.session_state.current_chat_id = chat_id
            if not any(c.get("id") == chat_id for c in st.session_state.conversations):
                st.session_state.conversations.append({"id": chat_id, "title": st.session_state.current_chat_title})
        st.session_state.chat_history.append(
            {
                "question": f"Code analysis ({language}): {code_action}",
                "answer": response,
                "sources": [],
                "metadata": [],
            }
        )
        st.rerun()

# -------------------------
# Chat input for follow-up questions
# -------------------------
question = st.chat_input("Ask anything...")
if question:
    normalized_question = question.strip().lower()

    if st.session_state.active_context_type == "document":
        broad_queries = {
            "summary",
            "summarize",
            "summarise",
            "what is this pdf about",
            "what is this document about",
            "explain this pdf",
            "explain this document",
            "overview",
        }

        if normalized_question in broad_queries:
            question = (
                "Provide a comprehensive summary of the uploaded document, "
                "including its main topics, key points, and purpose."
            )

        with st.spinner("🤖 Thinking..."):

            query_embedding = embed_query(question)

            results = search(
                query_embedding=query_embedding,
                n_results=20,
            )

            documents = results.get("documents", [])
            metadatas = results.get("metadatas", [])

            if (
                not documents
                or len(documents) == 0
                or len(documents[0]) == 0
            ):
                answer = "I couldn't find any relevant information in the uploaded documents."

                if st.session_state.current_chat_title == "New Chat":
                    title_candidate = question.strip()[:40]
                    st.session_state.current_chat_title = title_candidate
                    chat_id = st.session_state.current_chat_id or str(uuid.uuid4())
                    st.session_state.current_chat_id = chat_id
                    if not any(c.get("id") == chat_id for c in st.session_state.conversations):
                        st.session_state.conversations.append({"id": chat_id, "title": st.session_state.current_chat_title})

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer,
                        "sources": [],
                        "metadata": [],
                    }
                )

                st.rerun()

            else:

                # --------------------------------------------------
                # Build context from all uploaded documents whenever
                # possible. Fall back to semantic retrieval for
                # larger collections.
                # --------------------------------------------------

                retrieved_context = "\n\n".join(documents[0])

                full_document_context = st.session_state.get(
                    "active_context",
                    "",
                )

                # If the combined uploaded text fits, use it so the
                # model can answer across multiple uploaded files.
                if full_document_context and len(full_document_context) <= 12000:
                    context = full_document_context
                else:
                    context = retrieved_context

                # Prevent extremely large prompts
                MAX_CONTEXT_CHARS = 30000
                if len(context) > MAX_CONTEXT_CHARS:
                    context = context[:MAX_CONTEXT_CHARS]

                try:
                    answer = ask_llm(
                        context=context,
                        question=question,
                    )
                except Exception as e:
                    answer = f"An AI error occurred: {e}"

                if st.session_state.current_chat_title == "New Chat":
                    title_candidate = question.strip()[:40]
                    st.session_state.current_chat_title = title_candidate
                    chat_id = st.session_state.current_chat_id or str(uuid.uuid4())
                    st.session_state.current_chat_id = chat_id
                    if not any(c.get("id") == chat_id for c in st.session_state.conversations):
                        st.session_state.conversations.append({"id": chat_id, "title": st.session_state.current_chat_title})

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
                st.rerun()

    elif st.session_state.active_context_type in {"text", "code"}:
        with st.spinner("🤖 Thinking..."):
            try:
                answer = ask_llm(
                    context=st.session_state.active_context,
                    question=question,
                )
            except Exception as e:
                answer = f"An AI error occurred: {e}"

            if st.session_state.current_chat_title == "New Chat":
                title_candidate = question.strip()[:40]
                st.session_state.current_chat_title = title_candidate
                chat_id = st.session_state.current_chat_id or str(uuid.uuid4())
                st.session_state.current_chat_id = chat_id
                if not any(c.get("id") == chat_id for c in st.session_state.conversations):
                    st.session_state.conversations.append({"id": chat_id, "title": st.session_state.current_chat_title})

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer,
                    "sources": [],
                    "metadata": [],
                }
            )
            st.rerun()

    else:
        with st.spinner("🤖 Thinking..."):
            try:
                answer = ask_llm(
                    context="",
                    question=question,
                )
            except Exception as e:
                answer = f"An AI error occurred: {e}"

            if st.session_state.current_chat_title == "New Chat":
                title_candidate = question.strip()[:40]
                st.session_state.current_chat_title = title_candidate
                chat_id = st.session_state.current_chat_id or str(uuid.uuid4())
                st.session_state.current_chat_id = chat_id
                if not any(c.get("id") == chat_id for c in st.session_state.conversations):
                    st.session_state.conversations.append({"id": chat_id, "title": st.session_state.current_chat_title})

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer,
                    "sources": [],
                    "metadata": [],
                }
            )
            st.rerun()

# -------------------------
# Footer
# -------------------------
render_footer()