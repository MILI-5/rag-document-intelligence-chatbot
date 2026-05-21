from core.embeddings.embedding_model import get_embedding_model

embeddings = get_embedding_model()

vector = embeddings.embed_query("What is Retrieval-Augmented Generation?")

print(f"Vector length: {len(vector)}")
print(vector[:5])