import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from core.embeddings.retriever import load_retriever
from core.utils.logger import get_logger

# ---------------- LOAD ENV ----------------
load_dotenv()

logger = get_logger()

# ---------------- API KEY ----------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        "Create a .env file in the project root and add:\n"
        "GROQ_API_KEY=your_groq_api_key"
    )

print("GROQ API KEY LOADED SUCCESSFULLY")

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer ONLY using the context below.

Context:
{context}
"""

# ---------------- LLM ----------------
def get_llm():
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama3-8b-8192",
        temperature=0,
        streaming=True
    )

llm = get_llm()

# ---------------- RETRIEVAL ----------------
def retrieve_documents(query):

    logger.info(f"Retrieving documents for query: {query}")

    retriever = load_retriever()

    docs = retriever.get_relevant_documents(query)

    return [(doc, 0.0) for doc in docs]

# ---------------- STREAMING FUNCTION ----------------
def stream_answer(query: str):

    try:
        logger.info(f"Streaming answer for query: {query}")

        retrieved_docs = retrieve_documents(query)

        if not retrieved_docs:
            return iter([
                type(
                    "obj",
                    (object,),
                    {"content": "No relevant documents found."}
                )
            ]), []

        context = "\n\n".join(
            [doc.page_content for doc, _ in retrieved_docs]
        )

        prompt = SYSTEM_PROMPT.format(
            context=context
        ) + f"\nQuestion: {query}"

        return llm.stream(prompt), retrieved_docs

    except Exception as e:

        logger.error(f"Error in stream_answer: {str(e)}")

        return iter([
            type(
                "obj",
                (object,),
                {"content": f"System error: {str(e)}"}
            )
        ]), []

# ---------------- CITATIONS ----------------
def format_citations(retrieved_docs):

    citation_text = "\n\n### Sources\n"

    for i, (doc, score) in enumerate(retrieved_docs):

        page = doc.metadata.get("page", "Unknown")

        citation_text += (
            f"\n**Source {i+1}** "
            f"(Page {page}, Score: {score:.2f})"
        )

    return citation_text

# ---------------- MAIN GENERATION ----------------
def generate_answer(query: str):

    try:
        logger.info(f"Generating answer for: {query}")

        retrieved_docs = retrieve_documents(query)

        if not retrieved_docs:
            return {
                "answer": "I don't know based on the provided documents.",
                "sources": []
            }

        context = "\n\n".join(
            [doc.page_content for doc, _ in retrieved_docs]
        )

        prompt = SYSTEM_PROMPT.format(
            context=context
        ) + f"\nQuestion: {query}"

        response = llm.invoke(prompt)

        citation_text = format_citations(retrieved_docs)

        return {
            "answer": response.content + citation_text,
            "sources": retrieved_docs
        }

    except Exception as e:

        logger.error(f"System error: {str(e)}")

        return {
            "answer": f"System error: {str(e)}",
            "sources": []
        }