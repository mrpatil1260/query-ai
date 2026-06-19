from app.services.embedding_service import embed_texts

texts = [
    "Python is a programming language.",
    "FastAPI is a modern web framework."
]

embeddings = embed_texts(texts)

print(f"Number of embeddings: {len(embeddings)}")
print(f"Dimension of first embedding: {len(embeddings[0])}")
print("First 10 values of first embedding:")
print(embeddings[0][:10])