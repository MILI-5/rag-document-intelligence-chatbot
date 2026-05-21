from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from core.embeddings.vector_store import load_vector_store
from core.generations.prompt_templates import SYSTEM_PROMPT

load_dotenv()


def build_qa_chain():

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10
        }
    )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0,
        streaming=True
    )

    prompt_template = PromptTemplate(
        template=SYSTEM_PROMPT + "\nQuestion: {question}",
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt_template
        }
    )

    return qa_chain