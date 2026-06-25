from app.services.chroma_service import (
    reset_collection,
    add_documents,
    search,
)


def test_add_and_search_documents():
    # Start with a clean collection
    reset_collection()

    ids = ["doc1"]

    texts = [
        "Artificial Intelligence is transforming software engineering."
    ]

    # 384 dimensions for all-MiniLM-L6-v2
    embeddings = [[0.1] * 384]

    add_documents(
        ids=ids,
        texts=texts,
        embeddings=embeddings,
        source_name="test.pdf",
    )

    results = search(
        query_embedding=[0.1] * 384,
        n_results=1,
    )

    assert "documents" in results
    assert len(results["documents"]) > 0
    assert len(results["documents"][0]) >= 1

    assert (
        "Artificial Intelligence"
        in results["documents"][0][0]
    )


def test_reset_collection():
    reset_collection()

    results = search(
        query_embedding=[0.1] * 384,
        n_results=1,
    )

    assert "documents" in results