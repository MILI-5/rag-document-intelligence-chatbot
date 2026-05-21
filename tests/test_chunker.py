from core.ingestion.loader import load_pdf
from core.ingestion.chunker import split_documents

docs = load_pdf("data/uploads/sample.pdf")

chunks = split_documents(docs)

print(chunks[0].page_content)
print(chunks[0].metadata)