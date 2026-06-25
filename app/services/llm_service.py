import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(
    context: str,
    question: str,
    system_prompt: str | None = None,
) -> str:
    """
    Query AI document assistant.
    Answers strictly from uploaded documents while allowing
    summarization and reasoning across the provided context.
    """

    has_context = bool(context and context.strip())

    if system_prompt is None:
        if has_context:
            system_prompt = """
You are Query AI, an intelligent document assistant.

Your job is to answer questions using ONLY the provided document context.

Instructions:
- Read the entire context carefully.
- You MAY summarize, explain, and combine information from multiple sections.
- For questions like:
  - "Summarize the document"
  - "What is this PDF about?"
  - "Explain this resume"
  - "What are the key points?"
  provide a concise, well-structured answer based entirely on the supplied context.
- Do NOT invent facts or use outside knowledge.
- If the answer truly cannot be inferred from the context, respond:
  "I couldn't find enough information in the uploaded documents to answer that question."
- Use bullet points where appropriate.
- Keep answers clear and professional.
"""
        else:
            system_prompt = """
You are Query AI, a helpful AI assistant.

Your job is to answer general questions clearly and concisely.

You do not have access to any uploaded documents, so answer based on your general knowledge.

Keep answers clear and professional.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"""
Document Context:

{context}

User Question:

{question}

Provide the best possible answer using only the document context.
""" if has_context else f"User Question:\n\n{question}"
                ),
            },
        ],
    )

    return response.choices[0].message.content.strip()