from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ---------------- EMBEDDING MODEL ----------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------- CREATE VECTOR STORE ----------------
def create_vector_store(chunks):

    if not chunks:
        raise ValueError("No document chunks provided.")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embedding_model
    )

    return vector_store

# ---------------- SAVE VECTOR STORE ----------------
def save_vector_store(vector_store, save_path="faiss_index"):

    vector_store.save_local(save_path)

# ---------------- LOAD VECTOR STORE ----------------
def load_vector_store(save_path="faiss_index"):

    vector_store = FAISS.load_local(
        save_path,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return vector_store