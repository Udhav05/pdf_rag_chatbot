import faiss
import numpy as np
import pickle
import os
import requests
from sentence_transformers import SentenceTransformer

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

CHUNKS_FOLDER = 'chunks'

def load_index_and_metadata(index_path, meta_path):
    index = faiss.read_index(index_path)
    with open(meta_path, 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata

def search(query, index, metadata, top_k=5):
    query_embedding = model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for i in indices[0]:
        if i < len(metadata):
            results.append(metadata[i])
    return results

def build_prompt(query, retrieved_chunks):
    context_texts = []
    for chunk in retrieved_chunks:
        if isinstance(chunk, dict):
            filename = chunk.get('chunk_filename')
            page = chunk.get('page_num', 'Unknown')
        else:
            filename = chunk
            page = 'Unknown'

        if filename is None:
            continue

        chunk_path = os.path.join(CHUNKS_FOLDER, filename)
        if os.path.exists(chunk_path):
            with open(chunk_path, 'r', encoding='utf-8') as f:
                text = f.read().strip().replace('\n', ' ')
            context_texts.append(f"[File: {filename} | Page: {page}]\n{text}")
        else:
            context_texts.append(f"[File: {filename} | Page: {page}]\n[Chunk file not found]")

    context = "\n\n---\n\n".join(context_texts)
    prompt = f"""
You are an intelligent assistant. Use the following extracted document chunks to answer the question as accurately and concisely as possible.

Context:
{context}

Question: {query}
Answer:"""
    return prompt.strip()

def query_ollama(prompt, model_name="llama2"):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)  # Increased timeout
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"[Error communicating with Ollama API] {e}"

if __name__ == "__main__":
    index_path = "faiss.index"
    meta_path = "metadata.pkl"

    print("🔍 Loading index and metadata...")
    index, metadata = load_index_and_metadata(index_path, meta_path)

    print("✅ Ready to chat! Type your query or 'exit' to quit.")
    try:
        while True:
            query = input("\nEnter your query: ").strip()
            if query.lower() == 'exit':
                break

            retrieved_chunks = search(query, index, metadata, top_k=2)
            print("DEBUG: retrieved_chunks =", retrieved_chunks)

            # Print source chunks for transparency
            print("\n📄 Source Chunks Used:")
            for chunk in retrieved_chunks:
                if isinstance(chunk, dict):
                    print(f" - {chunk.get('chunk_filename')} (Page {chunk.get('page_num', 'Unknown')})")
                else:
                    print(f" - {chunk}")

            prompt = build_prompt(query, retrieved_chunks)
            print("\n🤖 Querying Ollama...")
            answer = query_ollama(prompt)

            print("\n" + "=" * 60)
            print("📘 Answer:")
            print(answer)
            print("=" * 60)
    except KeyboardInterrupt:
        print("\n👋 Exiting gracefully.")
