from sentence_transformers import SentenceTransformer

# Load the embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    """
    Convert a list of text chunks into embeddings.
    """
    return model.encode(texts).tolist()


def embed_query(query):
    """
    Convert a single query into an embedding.
    """
    return model.encode(query).tolist()