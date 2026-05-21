from core.retrieval.retriever import retrieve_documents

results = retrieve_documents(
    "Summarize the document"
)

for doc, score in results:
    print("=" * 50)
    print("Score:", score)
    print(doc.metadata)
    print(doc.page_content[:400])
