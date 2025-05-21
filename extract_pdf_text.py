# extract_pdf_text.py
import fitz  # PyMuPDF
import os

def extract_text_by_page(pdf_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        file_name = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{page_num+1}.txt"
        with open(os.path.join(output_folder, file_name), "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved text of page {page_num+1} to {file_name}")

if __name__ == "__main__":
    pdf_folder = "pdfs"  # folder containing PDFs
    output_folder = "extracted_texts"
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf_file)
            print(f"Extracting pages from: {pdf_file}")
            extract_text_by_page(pdf_path, output_folder)
