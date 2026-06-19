import os
import streamlit as st

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from app.services.embedding_service import embed_texts, embed_query
from app.services.chroma_service import add_documents, search, reset_collection
from app.services.llm_service import ask_llm

st.set_page_config(page_title="AI Knowledge Assistant")

st.title("📚 AI Knowledge Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:

    upload_path = os.path.join(
        "data",
        "uploads",
        uploaded_file.name
    )

    with open(upload_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF uploaded successfully!")

    # Extract text
    text = extract_text_from_pdf(upload_path)

    # Split into chunks
    chunks = chunk_text(text)

    # Create embeddings
    embeddings = embed_texts(chunks)

    # Store in ChromaDB
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    reset_collection()



    add_documents(
        ids=ids,
        texts=chunks,
        embeddings=embeddings
    )

    st.success(f"Indexed {len(chunks)} chunks!")

    question = st.text_input("Ask a question about the PDF")

    if question:

        query_embedding = embed_query(question)

        results = search(query_embedding)

        context = "\n".join(results["documents"][0])

        answer = ask_llm(
            context=context,
            question=question
        )

        st.subheader("Answer")
        st.write(answer)