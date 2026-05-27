import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import requests

CHUNKS_FOLDER = "data/chunks"
INDEX_PATH = "data/faiss.index"
META_PATH = "data/metadata.pkl"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_index():
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError("FAISS index not found. Run build_index.py first.")

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def search(query, index, metadata, top_k=5):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, top_k)

    results = []
    for i in indices[0]:
        if i < len(metadata):
            results.append(metadata[i])
    return results


def build_context(retrieved_chunks):
    context = []

    for item in retrieved_chunks:
        file_name = item["chunk_filename"]
        page = item.get("page_num", "Unknown")

        file_path = os.path.join(CHUNKS_FOLDER, file_name)

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            context.append(f"[Page {page}] {text}")

    return "\n\n".join(context)


def ask_llm(query, context):
    prompt = f"""
You are a helpful AI assistant.

Use the context below to answer the question.

Context:
{context}

Question: {query}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]