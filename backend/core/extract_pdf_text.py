import fitz  # PyMuPDF
import os


def extract_text_by_page(pdf_path: str, output_folder: str):
    """
    Extract text from PDF page by page and save each page as a .txt file
    """

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        file_name = f"{pdf_name}_page_{page_num + 1}.txt"
        file_path = os.path.join(output_folder, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text.strip())

        print(f"✅ Saved page {page_num + 1} → {file_name}")


def process_all_pdfs(pdf_folder="pdfs", output_folder="extracted_texts"):
    """
    Process all PDFs in a folder
    """

    if not os.path.exists(pdf_folder):
        print(f"❌ PDF folder not found: {pdf_folder}")
        return

    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    if not pdf_files:
        print("❌ No PDF files found")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"\n📄 Processing: {pdf_file}")
        extract_text_by_page(pdf_path, output_folder)


if __name__ == "__main__":
    process_all_pdfs()