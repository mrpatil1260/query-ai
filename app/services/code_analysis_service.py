from app.services.llm_service import ask_llm


def analyze_code(
    code: str,
    language: str,
    action: str,
) -> str:
    """
    Analyze source code using the LLM.
    """

    question = f"""
Programming Language:
{language}

Task:
{action}

Analyze the following code and provide a detailed response.
"""

    return ask_llm(
        context=code,
        question=question,
    )