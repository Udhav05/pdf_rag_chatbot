import os
import re

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def get_page_number_from_filename(filename):
    # Example: page_1.txt -> 1
    match = re.search(r'(\d+)', filename)
    if match:
        return int(match.group(1))
    else:
        return None

def process_texts(input_folder, output_folder, chunk_size=1000, overlap=200):
    os.makedirs(output_folder, exist_ok=True)

    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]

    metadata = []  # To store metadata for each chunk: filename + page number

    for txt_file in txt_files:
        txt_path = os.path.join(input_folder, txt_file)
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
            chunks = chunk_text(text, chunk_size, overlap)

        base_filename = os.path.splitext(txt_file)[0]
        page_num = get_page_number_from_filename(txt_file)

        for i, chunk in enumerate(chunks):
            chunk_filename = f"{base_filename}_chunk_{i+1}.txt"
            chunk_path = os.path.join(output_folder, chunk_filename)
            with open(chunk_path, 'w', encoding='utf-8') as cf:
                cf.write(chunk)

            # Add metadata entry for this chunk
            metadata.append({
                'chunk_filename': chunk_filename,
                'page_num': page_num
            })

            print(f"Saved chunk: {chunk_filename}, page: {page_num}")

    # Save metadata to disk for later use
    import pickle
    with open('metadata.pkl', 'wb') as f:
        pickle.dump(metadata, f)

if __name__ == "__main__":
    input_folder = "texts"
    output_folder = "chunks"
    process_texts(input_folder, output_folder)
