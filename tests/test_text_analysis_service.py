from unittest.mock import patch

from app.services.text_analysis_service import analyze_text


@patch("app.services.text_analysis_service.ask_llm")
def test_summarize_action(mock_ask_llm):
    mock_ask_llm.return_value = "Short summary."

    result = analyze_text(
        text="This is a long document.",
        action="Summarize",
    )

    assert result == "Short summary."
    mock_ask_llm.assert_called_once()


@patch("app.services.text_analysis_service.ask_llm")
def test_unknown_action_uses_default_prompt(mock_ask_llm):
    mock_ask_llm.return_value = "Processed."

    result = analyze_text(
        text="Hello world",
        action="Custom Action",
    )

    assert result == "Processed."
    mock_ask_llm.assert_called_once()


@patch("app.services.text_analysis_service.ask_llm")
def test_generate_keywords(mock_ask_llm):
    mock_ask_llm.return_value = "- AI\n- Python\n- RAG"

    result = analyze_text(
        text="AI with Python and Retrieval-Augmented Generation.",
        action="Generate Keywords",
    )

    assert "AI" in result
    assert "Python" in result