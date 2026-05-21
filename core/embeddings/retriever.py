from core.embeddings.vector_store import load_vector_store


def load_retriever():
    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    return retriever