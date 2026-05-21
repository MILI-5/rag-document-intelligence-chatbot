import streamlit as st


def render_feedback(query: str, answer: str):

    st.markdown("---")
    st.subheader("💬 Was this answer helpful?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Yes"):
            st.success("Thanks for your feedback!")

    with col2:
        if st.button("👎 No"):
            st.warning("Thanks! We'll improve the response.")
            