# search.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_index_and_metadata(index_path, meta_path):
    index = faiss.read_index(index_path)
    with open(meta_path, 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata

def search(query, index, metadata, top_k=5):
    query_embedding = model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for idx in indices[0]:
        chunk_info = metadata[idx]
        results.append(chunk_info)
    return results

if __name__ == "__main__":
    index_path = 'faiss.index'
    meta_path = 'metadata.pkl'

    index, metadata = load_index_and_metadata(index_path, meta_path)

    while True:
        query = input("\nEnter your query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        results = search(query, index, metadata)
        print("Top matching chunks with page numbers:")
        for res in results:
            print(f"- {res['chunk_filename']} (Page: {res['page_num']})")
