import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

# Load SentenceTransformer model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_chunks(chunk_folder):
    chunks = []
    metadata = []
    for file_name in os.listdir(chunk_folder):
        if file_name.endswith('.txt'):
            path = os.path.join(chunk_folder, file_name)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
                chunks.append(text)
                metadata.append(file_name)
    return chunks, metadata

def embed_chunks(chunks):
    embeddings = model.encode(chunks, show_progress_bar=True)
    return np.array(embeddings).astype('float32')

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)  # L2 distance metric
    index.add(embeddings)            # add embeddings to the index
    return index

def save_index(index, path):
    faiss.write_index(index, path)

def save_metadata(metadata, path):
    with open(path, 'wb') as f:  # 'wb' for write binary
        pickle.dump(metadata, f)

if __name__ == "__main__":
    chunk_folder = 'chunks'        # Folder where chunked text files are stored
    index_path = 'faiss.index'     # FAISS index file name
    meta_path = 'metadata.pkl'     # Metadata (filenames) file name

    chunks, metadata = load_chunks(chunk_folder)    # Load text chunks and filenames
    embeddings = embed_chunks(chunks)                # Get embeddings for each chunk
    index = build_faiss_index(embeddings)            # Build FAISS index
    save_index(index, index_path)                      # Save index to disk
    save_metadata(metadata, meta_path)                 # Save metadata to disk

    print("Index and metadata saved successfully!")
