import streamlit as st


def render_resume_workspace():
    """
    Render the Resume Review workspace.

    Returns:
        tuple:
            (
                uploaded_resume,
                target_role,
                job_description,
                analyze_button_clicked,
            )
    """

    st.header("📄 AI Resume Review")
    st.caption(
        "Upload your resume and optionally provide a target role and job description "
        "to receive personalized AI-powered feedback."
    )

    # Upload resume
    uploaded_resume = st.file_uploader(
        "📄 Upload Resume (PDF)",
        type=["pdf"],
        key="resume_uploader",
    )

    # Target role selection
    target_role = st.selectbox(
        "🎯 Target Role",
        [
            "Java Backend Developer",
            "Python Developer",
            "Full Stack Developer",
            "AI Engineer",
            "Machine Learning Engineer",
            "Data Analyst",
            "Data Scientist",
            "Software Engineer",
            "DevOps Engineer",
            "Other",
        ],
        key="target_role",
    )

    # Job description input
    job_description = st.text_area(
        "💼 Job Description (Optional)",
        height=250,
        placeholder=(
            "Paste the job description here.\n\n"
            "Query AI will compare your resume against it and identify:\n"
            "• Missing skills\n"
            "• Resume improvements\n"
            "• Keyword gaps\n"
            "• Tailored interview questions\n"
            "• ATS-friendly suggestions"
        ),
        key="job_description",
    )

    analyze = st.button(
        "🚀 Analyze Resume",
        key="analyze_resume_button",
        use_container_width=True,
    )

    return (
        uploaded_resume,
        target_role,
        job_description,
        analyze,
    )