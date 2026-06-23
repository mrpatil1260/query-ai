from functools import lru_cache
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_model():
    """
    Load the embedding model only once and reuse it.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    """
    Convert a list of text chunks into embeddings.
    """
    model = get_model()
    return model.encode(texts).tolist()


def embed_query(query):
    """
    Convert a single query into an embedding.
    """
    model = get_model()
    return model.encode(query).tolist()