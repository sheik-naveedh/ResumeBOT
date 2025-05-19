# Resume Parser RAG Chatbot

This project is a local Retrieval-Augmented Generation (RAG) based chatbot that parses resumes in PDF format and allows users to ask questions about the candidate's qualifications. It combines document retrieval and generative AI using LangChain, a local Hugging Face model, and FAISS for semantic search.

## Project Objective

To build a smart application that enables users to:

* Upload a resume in PDF format
* Ask questions like "What are the candidate's skills?" or "Does the person have a master's degree?"
* Get accurate answers using the uploaded document content

## Tech Stack

### Backend

* **Flask** – Lightweight server for handling uploads and query endpoints
* **LangChain** – Framework for orchestrating LLMs and retrieval
* **PyMuPDF** – For parsing text from PDF resumes
* **FAISS** – Fast vector similarity search
* **Hugging Face Transformers** – Local language model (Falcon RW-1B)
* **Sentence Transformers** – Embedding generation (`all-MiniLM-L6-v2`)

### Frontend

* **Streamlit** – UI for uploading resumes and interacting with the chatbot

## Features

* Upload resume PDFs directly via UI
* Ask natural language questions about resume content
* Local LLM inference (no external API dependency)
* Fast, context-aware answers using RAG pipeline
* Clean and readable answer formatting

## Project Structure

```
.
├── app.py                # Flask backend (PDF upload + query endpoints)
├── llm_loader.py         # Loads local Falcon model
├── rag_pipeline.py       # Builds RAG pipeline (split + embed + retrieve)
├── frontend_app.py       # Streamlit frontend app
├── pdfs/                 # Uploaded resumes
├── requirements.txt      # Python dependencies
```

## How it Works

1. **Upload**: User uploads a resume PDF via the Streamlit interface.
2. **Ingestion**: The backend reads the PDF using PyMuPDF and splits it into overlapping chunks.
3. **Embedding**: Each chunk is embedded using `all-MiniLM-L6-v2` from Sentence Transformers.
4. **Storage**: The embeddings are stored in a FAISS vector database.
5. **Query**: When a user asks a question, FAISS retrieves relevant chunks.
6. **Response**: The Falcon RW-1B model generates a context-aware answer using LangChain's `RetrievalQA`.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/resume-parser-rag-chatbot.git
cd resume-parser-rag-chatbot
```

### 2. Install Dependencies

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then install requirements:

```bash
pip install -r requirements.txt
```

### 3. Run Backend (Flask)

```bash
python app.py
```

### 4. Run Frontend (Streamlit)

```bash
streamlit run frontend_app.py
```

### 5. Access the App

Open your browser and go to:
[http://localhost:8501](http://localhost:8501)

## Notes

* The app currently runs entirely on your local machine.
* Falcon RW-1B is a small model for lightweight inference. For production, you can swap it for a larger model if GPU resources are available.
* FAISS indexes are reset each time a new PDF is uploaded.

## License

This project is open-source under the [MIT License](LICENSE).
