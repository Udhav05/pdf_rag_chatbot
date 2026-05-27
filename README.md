

# 📄 PDF RAG Chatbot (AI Document Assistant)

A full-stack **Retrieval-Augmented Generation (RAG) chatbot** that allows users to upload PDFs and ask questions based on their content using AI.

It combines **FastAPI, React, FAISS, and Sentence Transformers** to build an intelligent document Q&A system.

---

# 🚀 Features

* 📄 Upload PDF documents
* ✂️ Automatic text extraction from PDFs
* 🔗 Chunking for better retrieval
* 🧠 Vector embeddings using Sentence Transformers
* 🔍 Semantic search using FAISS
* 🤖 AI-powered answer generation (LLM via Ollama / local model)
* 💬 Chat-like interface for Q&A
* ⚡ Fast API backend + React frontend

---

# 🏗️ Tech Stack

### Backend

* FastAPI
* FAISS (Vector Database)
* Sentence Transformers
* PyMuPDF
* Python

### Frontend

* React.js
* JavaScript
* Fetch API

### AI / NLP

* Sentence Transformers (`all-MiniLM-L6-v2`)
* Ollama / LLM integration

---

# 📁 Project Structure

```
pdf_rag_chatbot/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── rag_service.py
│   │
│   ├── utils/
│   │   ├── extract_pdf_text.py
│   │   ├── chunk_text.py
│   │   ├── faiss_index.py
│   │
│   ├── data/
│   │   ├── pdfs/
│   │   ├── extracted_texts/
│   │   ├── chunks/
│   │   ├── faiss.index
│   │   ├── metadata.pkl
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│
├── tests/
├── .gitignore
└── README.md
```

---

# ⚙️ Installation & Setup

## 1. Clone repository

```bash
git clone https://github.com/Udhav05/pdf_rag_chatbot.git
cd pdf_rag_chatbot
```

---

## 2. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## 3. Frontend setup

```bash
cd frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

# 🔄 How It Works

1. Upload PDF → backend extracts text
2. Text is split into chunks
3. Chunks are converted into embeddings
4. Stored in FAISS index
5. User asks question
6. Query is embedded and searched in FAISS
7. Relevant chunks are retrieved
8. LLM generates final answer

---

# 🧠 RAG Pipeline

```
PDF → Text Extraction → Chunking → Embeddings → FAISS Index
                                                    ↓
User Query → Embedding → Similarity Search → Context → LLM → Answer
```

---

# 📌 API Endpoints

### Upload PDF

```
POST /upload
```

### Ask Question

```
POST /chat
```

---

# ⚠️ Known Issues (Work in Progress)

* Backend import paths may require cleanup
* FAISS index must be generated before chat
* UI improvements pending
* Error handling improvements ongoing

---

# 📈 Future Improvements

* Streamed responses (like ChatGPT)
* Multi-PDF support
* Authentication system
* Cloud deployment (Render / AWS)
* Better UI (chat bubbles, loading states)

---

# 👨‍💻 Author

**Udhav**

GitHub: [https://github.com/Udhav05](https://github.com/Udhav05)

