import streamlit as st
import requests

st.set_page_config(page_title="RAG PDF Chatbot", layout="centered")
st.title("📄🧠 RAG PDF Chatbot")

backend_url = "http://localhost:5000"  # Change if backend runs elsewhere

st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading and processing PDF..."):
        files = {"pdf": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{backend_url}/upload", files=files)

        if response.status_code == 200:
            st.sidebar.success("PDF uploaded successfully ✅")
        else:
            st.sidebar.error("Failed to upload PDF ❌")
            st.sidebar.error(response.json().get("error", "Unknown error"))

st.markdown("### Ask a question about your PDF")

query = st.text_input("Your question")

if st.button("Submit Query") and query:
    with st.spinner("Thinking..."):
        try:
            res = requests.post(f"{backend_url}/query", json={"query": query})
            if res.status_code == 200:
                answer = res.json()["response"]
                st.success("Answer:")
                st.write(answer)
            else:
                st.error("Query failed ❌")
                st.error(res.json().get("error", "Unknown error"))
        except Exception as e:
            st.error(f"Connection error: {e}")
