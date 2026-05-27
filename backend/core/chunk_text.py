# chunk_text.py
import os
import pickle

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def process_pages(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    metadata = []

    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    for txt_file in txt_files:
        try:
            page_num = int(txt_file.split('_page_')[1].split('.txt')[0])
        except (IndexError, ValueError):
            page_num = None  # fallback if naming unexpected

        with open(os.path.join(input_folder, txt_file), 'r', encoding='utf-8') as f:
            text = f.read()

        chunks = chunk_text(text)
        base_name = os.path.splitext(txt_file)[0]

        for i, chunk in enumerate(chunks):
            chunk_filename = f"{base_name}_chunk_{i+1}.txt"
            chunk_path = os.path.join(output_folder, chunk_filename)
            with open(chunk_path, 'w', encoding='utf-8') as cf:
                cf.write(chunk)
            metadata.append({
                "chunk_filename": chunk_filename,
                "page_num": page_num
            })
            print(f"Saved chunk: {chunk_filename} (Page {page_num})")

    with open(os.path.join(output_folder, 'metadata.pkl'), 'wb') as f:
        pickle.dump(metadata, f)
    print("Metadata with page numbers saved!")

if __name__ == "__main__":
    input_folder = "extracted_texts"
    output_folder = "chunks"
    process_pages(input_folder, output_folder)
