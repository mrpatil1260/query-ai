

import streamlit as st


def render_uploader():
    """Render the PDF uploader section and return the uploaded file."""

    st.markdown("## 📤 Upload Document")
    st.caption("Upload a PDF to build your AI-powered knowledge base.")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
        help="Supported format: PDF",
    )

    return uploaded_file