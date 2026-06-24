import re

from app.utils.skills_catalog import TECH_SKILLS


def extract_skills(text: str) -> list[str]:
    """
    Deterministically extract known technical skills
    from text.
    """

    if not text:
        return []

    text_lower = text.lower()
    detected = set()

    for skill in TECH_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):
            detected.add(skill)

    return sorted(detected)