import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o-mini"

    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50

    TOP_K = 4

    VECTOR_STORE_PATH = "data/vector_store"
    UPLOAD_DIR = "data/uploads"