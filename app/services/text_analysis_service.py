from app.services.llm_service import ask_llm


def analyze_text(text: str, action: str) -> str:
    """
    Analyze user-provided text based on the selected action.
    """

    prompts = {
        "Summarize": (
            "Provide a concise and well-structured summary of the text."
        ),
        "Explain": (
            "Explain the text in simple and easy-to-understand language."
        ),
        "Extract Key Points": (
            "Extract the most important key points as bullet points."
        ),
    }

    question = prompts.get(
        action,
        "Analyze the following text.",
    )

    return ask_llm(
        context=text,
        question=question,
    )