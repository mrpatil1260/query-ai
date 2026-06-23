import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")

COLLECTION_NAME = "documents"


def get_collection():
    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def reset_collection():
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    return get_collection()


def add_documents(ids, texts, embeddings):
    collection = get_collection()

    metadatas = [
        {
            "chunk_index": i,
            "source": "uploaded_pdf",
        }
        for i in range(len(texts))
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search(query_embedding, n_results=5):
    collection = get_collection()

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )