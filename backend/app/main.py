from fastapi import FastAPI, UploadFile, File
import shutil
import os

from backend.app.rag_service import load_index, search, build_context, ask_llm

app = FastAPI()

UPLOAD_FOLDER = "data/pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

index, metadata = load_index()


@app.get("/")
def home():
    return {"message": "RAG chatbot running"}


@app.get("/chat")
def chat(query: str):
    docs = search(query, index, metadata)
    context = build_context(docs)
    answer = ask_llm(query, context)

    return {
        "query": query,
        "answer": answer,
        "sources": docs
    }
@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "message": "File uploaded successfully",
        "filename": file.filename
    }