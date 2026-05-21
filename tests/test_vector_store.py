from core.ingestion.loader import load_pdf
from core.ingestion.chunker import split_documents

from core.embeddings.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store
)

docs = load_pdf("data/uploads/sample.pdf")

chunks = split_documents(docs)

vector_store = create_vector_store(chunks)

save_vector_store(vector_store)

loaded_store = load_vector_store()

results = loaded_store.similarity_search(
    "What is Sanjana studying?",
    k=2
)

for i, doc in enumerate(results):
    print(f"\nResult {i+1}:")
    print(doc.page_content)