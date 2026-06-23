import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(context: str, question: str) -> str:
    """
    Generate an answer using the retrieved document context.
    """

    prompt = f"""
You are an AI Knowledge Assistant.

Your task is to answer the user's question ONLY using the provided context.

Rules:
1. Use ONLY the information present in the context.
2. Do NOT use your own knowledge.
3. Do NOT make up facts or guess.
4. If the answer is not present in the context, respond exactly:
   "I cannot find that information in the uploaded document."
5. Keep answers concise, factual, and well-structured.

========================
CONTEXT
========================
{context}

========================
QUESTION
========================
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content.strip()