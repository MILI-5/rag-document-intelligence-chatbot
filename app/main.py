import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st

from ui.sidebar import render_sidebar
from ui.chat import initialize_chat, display_chat_history, add_message
from app.feedback import render_feedback

from core.ingestion.file_manager import save_uploaded_file
from core.ingestion.loader import load_pdf
from core.ingestion.chunker import split_documents

from core.embeddings.vector_store import (
    create_vector_store,
    save_vector_store
)

from core.generations.generator import stream_answer, format_citations, generate_answer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="📄",
    layout="wide"
)


# ---------------- LOAD CSS ----------------
def load_css():
    css_path = os.path.join("app", "ui", "styles.css")

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# ---------------- CACHE ----------------
@st.cache_data(show_spinner=False)
def cached_response(query: str):
    return generate_answer(query)


# ---------------- UI INIT ----------------
settings = render_sidebar()

st.title("📄 RAG Document Intelligence Chatbot")

initialize_chat()


# ---------------- LAYOUT (STEP 5H) ----------------
left, right = st.columns([2, 1])


# =========================================================
# LEFT COLUMN → CHAT
# =========================================================
with left:

    display_chat_history()

    user_input = st.chat_input("Ask a question about the document...")

    if user_input:

        add_message("user", user_input)

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            response_placeholder = st.empty()
            full_response = ""

            cached_output = cached_response(user_input)

            # ---------------- CACHE HIT ----------------
            if isinstance(cached_output, dict) and "answer" in cached_output:

                final_answer = cached_output["answer"]
                response_placeholder.markdown(final_answer)

            # ---------------- STREAMING ----------------
            else:

                stream, retrieved_docs = stream_answer(user_input)

                for chunk in stream:
                    if chunk.content:
                        full_response += chunk.content
                        response_placeholder.markdown(full_response)

                citation_text = format_citations(retrieved_docs)

                final_answer = full_response + citation_text

                response_placeholder.markdown(final_answer)

            add_message("assistant", final_answer)

            render_feedback(user_input, final_answer)


# =========================================================
# RIGHT COLUMN → SETTINGS / SOURCES PANEL
# =========================================================
with right:

    st.subheader("⚙️ Settings & Info")

    uploaded_file = settings["uploaded_file"]

    if uploaded_file:

        with st.spinner("Processing PDF..."):

            file_path = save_uploaded_file(uploaded_file)
            docs = load_pdf(file_path)

            chunks = split_documents(
                docs,
                chunk_size=settings["chunk_size"],
                chunk_overlap=settings["chunk_overlap"]
            )

            vector_store = create_vector_store(chunks)
            save_vector_store(vector_store)

        st.success("PDF processed successfully!")

    st.markdown("---")
    st.subheader("📌 Tips")

    st.write("- Upload PDF in sidebar")
    st.write("- Ask questions in chat")
    st.write("- Cached answers are instant")

    st.markdown("---")
    st.subheader("📚 Sources")
    st.write("Sources appear inside chat responses")