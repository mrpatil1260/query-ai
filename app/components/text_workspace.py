import streamlit as st


def render_text_workspace():
    """
    Render the Text Workspace.
    Returns:
        tuple[str, str] -> (input_text, selected_action)
    """

    st.header("📝 Text Workspace")
    st.caption("Paste any text and let Query AI analyze it.")

    input_text = st.text_area(
        "Paste your text here",
        height=300,
        placeholder="Paste notes, articles, documentation, emails, or any text...",
    )

    action = st.radio(
        "Choose an action",
        options=[
            "Summarize",
            "Explain",
            "Extract Key Points",
        ],
        horizontal=True,
    )

    return input_text, action