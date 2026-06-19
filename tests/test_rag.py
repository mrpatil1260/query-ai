from app.services.embedding_service import embed_query
from app.services.chroma_service import search
from app.services.llm_service import ask_llm

question = "What is Python?"

# Convert question to embedding
query_embedding = embed_query(question)

# Retrieve relevant chunks
results = search(query_embedding)

# Combine retrieved text into context
context = "\n".join(results["documents"][0])

# Ask the LLM
answer = ask_llm(context, question)

print("\n===== CONTEXT =====\n")
print(context)

print("\n===== ANSWER =====\n")
print(answer)
