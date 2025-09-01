import streamlit as st
import requests
import time

# Change this to your deployed FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Frontend", layout="wide")

st.title("📚 RAG System - Streamlit Frontend")
st.write("Upload a file, ask questions, and get AI answers with citations.")

# --------------------------
# File Upload
# --------------------------
st.subheader("1️⃣ Upload Document")
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "csv", "docx"])

if uploaded_file is not None:
    if st.button("Upload to Backend"):
        with st.spinner("Uploading..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            res = requests.post(f"{API_URL}/upload/", files=files)

        if res.status_code == 200:
            st.success("✅ File uploaded successfully!")
        else:
            st.error("❌ Upload failed!")

# --------------------------
# Query Answering
# --------------------------
st.subheader("2️⃣ Ask a Question")
query = st.text_input("Enter your query")

if st.button("Get Answer"):
    if query.strip() == "":
        st.warning("⚠️ Please enter a question")
    else:
        with st.spinner("Fetching answer..."):
            start = time.time()
            res = requests.post(f"{API_URL}/query/", json={"query": query})
            end = time.time()

        if res.status_code == 200:
            data = res.json()

            st.write("### 📝 Answer")
            st.success(data.get("answer", "No answer found."))

            sources = data.get("sources", [])
            if sources:
                st.write("### 📌 Citations")
                for src in sources:
                    st.markdown(f"- {src}")

            st.info(f"⏱ Time Taken: {round(end-start,2)}s")
        else:
            st.error("❌ Query failed!")

# --------------------------
# Evaluation
# --------------------------
st.subheader("3️⃣ Evaluation Mode (5 Q/A Pairs)")

if st.button("Run Evaluation"):
    eval_set = [
        {"q": "What is AI?", "gold": "Artificial Intelligence is the simulation of human intelligence in machines."},
        {"q": "What is Machine Learning?", "gold": "Machine Learning is a subset of AI that learns from data."},
        {"q": "What is FastAPI?", "gold": "FastAPI is a modern, high-performance web framework for building APIs with Python."},
        {"q": "What is Pinecone?", "gold": "Pinecone is a vector database for similarity search and retrieval."},
        {"q": "What is RAG?", "gold": "Retrieval Augmented Generation combines retrieval and generation for better answers."},
    ]

    results = []
    for item in eval_set:
        res = requests.post(f"{API_URL}/query/", json={"query": item['q']})
        if res.status_code == 200:
            pred = res.json().get("answer", "")
            results.append((item['q'], pred, item['gold']))

    st.write("### ✅ Evaluation Results")
    for q, pred, gold in results:
        st.markdown(f"**Q:** {q}")
        st.markdown(f"- **Predicted:** {pred}")
        st.markdown(f"- **Expected:** {gold}")
        st.write("---")
