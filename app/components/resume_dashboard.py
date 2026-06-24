import streamlit as st


def render_resume_dashboard(result: dict):
    """
    Render a structured Resume Review dashboard.
    """



    st.subheader("📊 Resume Intelligence Dashboard")

    # -------------------------
    # Overall Match
    # -------------------------
    overall_match = result.get(
        "overall_match",
        "Not Available",
    )

    skills = result.get(
        "skills_found",
        [],
    )
    missing = result.get(
        "missing_skills",
        [],
    )
    missing_count = len(missing)

    if missing_count <= 2:
        match_badge = "🟢 Excellent Match"
    elif missing_count <= 5:
        match_badge = "🟡 Strong Match"
    elif missing_count <= 8:
        match_badge = "🟠 Moderate Match"
    else:
        match_badge = "🔴 Needs Improvement"

    st.markdown("### 🎯 Overall Assessment")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.metric(
            label="Resume Match",
            value=overall_match,
        )

    with col_b:
        st.markdown(f"### {match_badge}")

    keywords = result.get(
        "ats_keywords",
        [],
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🛠 Skills Found", value=len(skills))
    with col2:
        st.metric(label="❌ Missing Skills", value=len(missing))
    with col3:
        st.metric(label="🔑 ATS Keywords", value=len(keywords))

    st.divider()

    col1, col2 = st.columns(2)

    # -------------------------
    # Skills Found
    # -------------------------
    with col1:
        st.subheader("🛠 Skills Found")

        if skills:
            for skill in skills:
                st.markdown(f"- **{skill}**")
        else:
            st.info("No skills detected.")

    # -------------------------
    # Missing Skills
    # -------------------------
    with col2:
        st.subheader("⚠️ Missing Skills")

        if missing:
            for skill in missing:
                st.markdown(f"- **{skill}**")
        else:
            st.success("No missing skills identified.")
    # -------------------------
    # ATS Keywords
    # -------------------------
    st.subheader("🔑 Recommended Keywords")

    if keywords:
        for keyword in keywords:
            st.markdown(f"- **{keyword}**")
    else:
        st.info("No keyword recommendations.")

    # -------------------------
    # Skill Gap Summary
    # -------------------------
    with st.expander("📈 Skill Gap Summary", expanded=True):
        match_ratio = len(skills) / max(len(skills) + len(missing), 1)
        match_percentage = int(match_ratio * 100)

        st.write(f"**Resume Match:** {match_percentage}%")
        st.progress(match_ratio)

        st.write(f"✅ Matched Skills: {len(skills)}")
        st.write(f"❌ Missing Skills: {len(missing)}")
        if missing:
            st.warning("Focus on learning or highlighting the missing skills for a better match.")
        else:
            st.success("Great job! No major skill gaps detected.")

    # -------------------------
    # Strengths
    # -------------------------
    with st.expander("💪 Strengths", expanded=True):

        for item in result.get(
            "strengths",
            [],
        ):
            st.write(f"• {item}")

    # -------------------------
    # Improvements
    # -------------------------
    with st.expander("🔧 Areas for Improvement"):

        for item in result.get(
            "improvements",
            [],
        ):
            st.write(f"• {item}")

    # -------------------------
    # Action Plan
    # -------------------------
    with st.expander("📋 Personalized Action Plan"):
        if not result.get("action_plan", []):
            st.info("No personalized action items generated.")
        else:
            for item in result.get(
                "action_plan",
                [],
            ):
                st.write(f"• {item}")

    # -------------------------
    # Technical Questions
    # -------------------------
    with st.expander("🎤 Technical Interview Questions"):

        for question in result.get(
            "technical_questions",
            [],
        ):
            st.write(f"• {question}")

    # -------------------------
    # HR Questions
    # -------------------------
    with st.expander("🤝 HR Interview Questions"):

        for question in result.get(
            "hr_questions",
            [],
        ):
            st.write(f"• {question}")