import streamlit as st


def render_resume_result(result: str):
    """
    Display the AI-generated resume review
    inside a clean, styled container.
    """

    st.success("✅ Resume analysis complete!")

    st.markdown("## 📊 AI Resume Review")

    with st.container(border=True):
        st.markdown(result)