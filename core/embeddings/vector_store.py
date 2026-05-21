import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Folder where FAISS index will be stored
VECTOR_DB_PATH = "vectorstore/faiss_index"


# ---------------- CREATE VECTOR STORE ----------------
def create_vector_store(chunks):
    embeddings = OpenAIEmbeddings()

    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


# ---------------- SAVE VECTOR STORE ----------------
def save_vector_store(vector_store):
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    vector_store.save_local(VECTOR_DB_PATH)


# ---------------- LOAD VECTOR STORE ----------------
def load_vector_store():
    embeddings = OpenAIEmbeddings()

    vector_store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store