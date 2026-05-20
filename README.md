# Thesis Chatbot (Flask + RAG + Groq)

This project is a simple web app that lets users ask questions about a thesis document. It uses:
- **Flask** for the backend web server
- **Sentence-Transformers** to embed text
- **FAISS** for retrieval (similarity search over chunks of `data.txt`)
- **Groq LLM** to generate answers, with **streaming** back to the browser
- **Vanilla HTML/CSS/JS** for the frontend chat UI

---

## Project structure

- `app.py` – Flask server, FAISS index building, `/chat` endpoint with streaming
- `data.txt` – the knowledge base text to index and retrieve from
- `templates/index.html` – frontend page
- `static/style.css` – styling
- `static/script.js` – sends chat requests and renders streamed tokens
- `requirements.txt` – Python dependencies

---

## Prerequisites

- Python 3.9+ (3.10/3.11 recommended)
- A **Groq API key**

Create an environment variable:

- **Windows (PowerShell):**
  ```powershell
  setx GROQ_API_KEY "your_key_here"
  ```
  Then restart your terminal.

- **Windows (cmd.exe):**
  ```bat
  set GROQ_API_KEY=your_key_here
  ```
  (set only for the current terminal session)

---

## Setup and run (fresh clone)

### 1) Clone the repo
```bat
cd path\to\chatbot-web
```

### 2) (Recommended) Create a virtual environment
```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3) Install dependencies
```bat
pip install -r requirements.txt
```

### 4) Put your data in `data.txt`
- Ensure `data.txt` exists in the repo root.
- The app indexes it at server startup.

### 5) Start the server
```bat
python app.py
```

### 6) Open the UI
- Go to: **http://127.0.0.1:5000/**

---

## How it works (high level)

1. On startup, `app.py`:
   - reads `data.txt`
   - chunks it
   - embeds each chunk
   - builds a FAISS vector index
2. When you send a message to `/chat`:
   - embeds your query
   - retrieves top-k relevant chunks
   - builds a prompt with `Context` + `Question`
   - streams the Groq model response back to the browser

---

## Notes / common issues

- **Startup time**: FAISS indexing happens when `app.py` starts. For large `data.txt`, startup can take time.
- **Missing API key**: If `GROQ_API_KEY` is not set, Groq calls will fail.
- **Model downloads**: `SentenceTransformer("all-MiniLM-L6-v2")` downloads the embedding model the first time you run.

---

## Configuration

- Environment variable: `GROQ_API_KEY`
- Data file: `data.txt` (repo root)

---

