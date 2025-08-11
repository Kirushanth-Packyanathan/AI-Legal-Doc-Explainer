import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"

st.title("📄 AI Legal Document Explainer")

uploaded_file = st.file_uploader("Upload a legal document (PDF)", type=["pdf"])

if uploaded_file:
    if st.button("Summarize Document"):
        files = {"file": uploaded_file.getvalue()}
        res = requests.post(f"{FASTAPI_URL}/summarize", files={"file": uploaded_file})
        st.subheader("Summary")
        st.write(res.json()["summary"])

    st.subheader("Ask a Question")
    question = st.text_input("Enter your question")
    if st.button("Get Answer"):
        res = requests.post(f"{FASTAPI_URL}/ask",
                            files={"file": uploaded_file},
                            data={"question": question})
        st.write(res.json()["answer"])
