import json

from app.services.llm_service import ask_llm
from app.services.pdf_service import extract_text_from_pdf
from app.services.skill_extractor import extract_skills

def analyze_resume(
    pdf_path: str,
    target_role: str,
    job_description: str,
) -> dict:
    """
    Analyze a resume against a target role and optional
    job description.

    Returns a Python dictionary suitable for rendering
    in the Resume Dashboard.
    """

    resume_text = extract_text_from_pdf(pdf_path)

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = sorted(
        list(set(resume_skills) & set(job_skills))
    )

    missing_skills = sorted(
        list(set(job_skills) - set(resume_skills))
    )

    prompt = f"""
You are an expert technical recruiter.

Compare the resume with the target role and the job description.

Target Role:
{target_role}

Job Description:
{job_description if job_description.strip() else "Not provided."}

Computed Resume Skills:
{resume_skills}

Computed Job Description Skills:
{job_skills}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_skills}

Return ONLY valid JSON.

The JSON MUST follow exactly this schema:

{{
    "overall_match": "Strong",
    "skills_found": [],
    "missing_skills": [],
    "ats_keywords": [],
    "strengths": [],
    "improvements": [],
    "action_plan": [],
    "technical_questions": [],
    "hr_questions": []
}}

Populate:
- "skills_found" using the computed matched skills.
- "missing_skills" using the computed missing skills.
Base your recommendations and ATS keywords on these computed values and do not contradict them.
"""

    response = ask_llm(
        context=resume_text,
        question=prompt,
    )

    try:
        return json.loads(response)

    except Exception:
        # Fallback if the model returns invalid JSON
        return {
            "overall_match": "Unable to determine",
            "skills_found": matched_skills,
            "missing_skills": missing_skills,
            "ats_keywords": [],
            "strengths": [],
            "improvements": [
                "The AI response could not be parsed into structured data."
            ],
            "action_plan": [
                "Try running the analysis again."
            ],
            "technical_questions": [],
            "hr_questions": [],
        }