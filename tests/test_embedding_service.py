from unittest.mock import patch
from app.services.embedding_service import embed_texts, embed_query


class MockEmbedding:
    def __init__(self, value):
        self.value = value

    def tolist(self):
        return self.value


class MockModel:
    def encode(self, *args, **kwargs):
        if isinstance(args[0], list):
            # Simulate a NumPy array for multiple embeddings
            return MockEmbedding([
                [0.1, 0.2, 0.3],
                [0.4, 0.5, 0.6],
            ])

        # Simulate a NumPy array for a single embedding
        return MockEmbedding([0.1, 0.2, 0.3])


@patch("app.services.embedding_service.get_model")
def test_embed_texts_returns_embeddings(mock_get_model):
    mock_get_model.return_value = MockModel()

    texts = ["Hello world", "Query AI"]

    embeddings = embed_texts(texts)

    assert isinstance(embeddings, list)
    assert len(embeddings) == 2
    assert embeddings[0] == [0.1, 0.2, 0.3]


@patch("app.services.embedding_service.get_model")
def test_embed_query_returns_embedding(mock_get_model):
    mock_get_model.return_value = MockModel()

    embedding = embed_query("What is AI?")

    assert isinstance(embedding, list)
    assert embedding == [0.1, 0.2, 0.3]