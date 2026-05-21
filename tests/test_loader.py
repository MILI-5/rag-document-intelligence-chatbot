from core.ingestion.loader import load_pdf

docs = load_pdf("data/uploads/sample.pdf")

print(docs[0].page_content[:500])
print(docs[0].metadata)