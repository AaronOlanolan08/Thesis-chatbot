import os
import faiss
import numpy as np
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
from groq import Groq

# =========================
# LOAD ENV
# =========================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# =========================
# FLASK APP
# =========================
app = Flask(__name__)

# =========================
# MODELS
# =========================
embedder = SentenceTransformer("all-MiniLM-L6-v2")

LLM_MODEL = "llama-3.1-8b-instant"

FILE_PATH = "data.txt"

# =========================
# TEXT SPLIT
# =========================
def chunk_text(text, chunk_size=400, overlap=80):
    words = text.split()

    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]

# =========================
# EMBEDDINGS
# =========================
def embed_texts(texts):
    return embedder.encode(
        texts,
        convert_to_numpy=True
    ).astype("float32")

# =========================
# BUILD INDEX
# =========================
with open(FILE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_text(text)

embeddings = embed_texts(chunks)

faiss.normalize_L2(embeddings)

index = faiss.IndexFlatIP(embeddings.shape[1])

index.add(embeddings)

print("Document indexed!")

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

from flask import Response, stream_with_context, request

@app.route("/chat", methods=["POST"])
def chat():

    user_query = request.json["message"]

    # =========================
    # RETRIEVAL
    # =========================
    q_vec = embed_texts([user_query])
    faiss.normalize_L2(q_vec)

    _, I = index.search(q_vec, k=5)

    context = "\n\n".join(chunks[i] for i in I[0])

    # =========================
    # PROMPT
    # =========================
    prompt = f"""
Context:
{context}

Question:
{user_query}

Answer clearly and based only on context.
"""

    # =========================
    # STREAMING RESPONSE
    # =========================
    def generate():

        stream = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Use only the provided context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            stream=True   # 🔥 THIS IS THE KEY CHANGE
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content or ""
            if token:
                yield token

    return Response(stream_with_context(generate()), mimetype="text/plain")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)