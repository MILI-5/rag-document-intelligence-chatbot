from core.generations.llm_chain import build_qa_chain

qa_chain = build_qa_chain()

query = "What is this document about?"

response = qa_chain.invoke(
    {"query": query}
)

print("\nANSWER:\n")
print(response["result"])

print("\nSOURCES:\n")

for i, doc in enumerate(response["source_documents"]):

    print("=" * 60)

    print(f"Source {i+1}")

    print("Metadata:", doc.metadata)

    print(doc.page_content[:400])