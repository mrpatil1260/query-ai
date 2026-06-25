from app.services.chunk_service import chunk_text


def test_chunk_text_returns_list():
    text = "Hello world! " * 200
    chunks = chunk_text(text)

    assert isinstance(chunks, list)
    assert len(chunks) > 0


def test_chunk_text_preserves_content():
    text = "This is a test document for Query AI."
    chunks = chunk_text(text)

    combined = " ".join(chunks)

    assert "Query AI" in combined
    assert "test document" in combined


def test_chunk_text_splits_large_text():
    text = "Lorem ipsum " * 2000

    chunks = chunk_text(text)

    # Should produce multiple chunks
    assert len(chunks) > 1


def test_chunk_text_handles_empty_string():
    chunks = chunk_text("")

    assert isinstance(chunks, list)
    assert len(chunks) == 0


def test_chunk_text_handles_short_text():
    text = "Short text."

    chunks = chunk_text(text)

    assert len(chunks) == 1
    assert chunks[0] == text
