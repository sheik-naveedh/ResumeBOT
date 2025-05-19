from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re

from llm_loader import load_local_llm
from rag_pipeline import build_rag_pipeline

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

llm = load_local_llm()
qa_chain = None

@app.route("/upload", methods=["POST"])
def upload_pdf():
    global qa_chain

    if "pdf" not in request.files:
        return jsonify({"error": "No PDF uploaded"}), 400

    pdf_file = request.files["pdf"]
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_path)

    try:
        qa_chain = build_rag_pipeline(pdf_path, llm)
        return jsonify({"message": "PDF uploaded and processed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def remove_repeated_phrases(text):
    lines = text.splitlines()
    seen = set()
    result = []
    for line in lines:
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            result.append(line)
    cleaned = " ".join(result)
    cleaned = re.sub(r'(\b\w+\b)(?:\s+\1\b)+', r'\1', cleaned, flags=re.IGNORECASE)
    if "Answer:" in cleaned:
        cleaned = cleaned.split("Answer:")[-1].strip()
    return cleaned.strip()

@app.route("/query", methods=["POST"])
def query_pdf():
    global qa_chain

    if not qa_chain:
        return jsonify({"error": "No PDF uploaded yet"}), 400

    user_query = request.json.get("query")
    if not user_query:
        return jsonify({"error": "Query not provided"}), 400

    try:
        response = qa_chain.run(user_query)
        answer = remove_repeated_phrases(response)
        return jsonify({"response": answer}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)