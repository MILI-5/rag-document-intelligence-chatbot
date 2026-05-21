import streamlit as st


def render_sidebar():
    st.sidebar.title("⚙️ Settings")

    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    chunk_size = st.sidebar.slider(
        "Chunk Size",
        100,
        2000,
        500
    )

    chunk_overlap = st.sidebar.slider(
        "Chunk Overlap",
        0,
        500,
        50
    )

    return {
        "uploaded_file": uploaded_file,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap
    }