from core.generations.generator import generate_answer

query = "Summarize this document."

response = generate_answer(query)

print("\nANSWER:\n")

print(response["answer"])

print("\nSOURCES:\n")

for doc, score in response["sources"]:

    print("=" * 60)

    print("Score:", score)

    print("Metadata:", doc.metadata)

    print(doc.page_content[:400])