from unittest.mock import patch

from app.services.code_analysis_service import analyze_code


@patch("app.services.code_analysis_service.ask_llm")
def test_explain_code(mock_ask_llm):
    mock_ask_llm.return_value = "This code prints Hello World."

    result = analyze_code(
        code='print("Hello World")',
        language="Python",
        action="Explain Code",
    )

    assert result == "This code prints Hello World."
    mock_ask_llm.assert_called_once()


@patch("app.services.code_analysis_service.ask_llm")
def test_find_bugs(mock_ask_llm):
    mock_ask_llm.return_value = "No major bugs found."

    result = analyze_code(
        code="x = 1",
        language="Python",
        action="Find Bugs",
    )

    assert result == "No major bugs found."
    mock_ask_llm.assert_called_once()


@patch("app.services.code_analysis_service.ask_llm")
def test_unknown_action_uses_default(mock_ask_llm):
    mock_ask_llm.return_value = "Processed successfully."

    result = analyze_code(
        code="console.log('Hello')",
        language="JavaScript",
        action="Custom Action",
    )

    assert result == "Processed successfully."
    mock_ask_llm.assert_called_once()
    