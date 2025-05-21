# embed_and_index.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_chunks_and_metadata(chunk_folder):
    chunks = []
    metadata = []

    with open(os.path.join(chunk_folder, 'metadata.pkl'), 'rb') as f:
        metadata = pickle.load(f)

    for meta in metadata:
        chunk_path = os.path.join(chunk_folder, meta["chunk_filename"])
        with open(chunk_path, 'r', encoding='utf-8') as f:
            text = f.read()
            chunks.append(text)

    return chunks, metadata

def embed_chunks(chunks):
    embeddings = model.encode(chunks, show_progress_bar=True)
    return np.array(embeddings).astype('float32')

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def save_index(index, path):
    faiss.write_index(index, path)

def save_metadata(metadata, path):
    with open(path, 'wb') as f:
        pickle.dump(metadata, f)

if __name__ == "__main__":
    chunk_folder = 'chunks'
    index_path = 'faiss.index'
    meta_path = 'metadata.pkl'

    chunks, metadata = load_chunks_and_metadata(chunk_folder)
    embeddings = embed_chunks(chunks)
    index = build_faiss_index(embeddings)
    save_index(index, index_path)
    save_metadata(metadata, meta_path)

    print("FAISS index and metadata saved successfully!")
