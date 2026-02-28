# rag_pipeline.py — Module 19
"""
A self-contained RAG (Retrieval-Augmented Generation) pipeline.

Requirements:
    pip install ollama chromadb
    ollama pull llama3.2
    ollama pull nomic-embed-text
"""

import ollama
import chromadb

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL  = "llama3.2"

# ── Step 1: Set up the vector store ──────────────────────────────────────

client     = chromadb.Client()
collection = client.get_or_create_collection("course_docs")


# ── Step 2: Index documents ───────────────────────────────────────────────

def index_documents(documents: list[str]) -> None:
    """Embed and store each document in the vector store."""
    for i, doc in enumerate(documents):
        embedding = ollama.embeddings(model=EMBED_MODEL, prompt=doc)["embedding"]
        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[f"doc_{i}"],
        )
    print(f"Indexed {len(documents)} documents.")


# ── Step 3: Search ────────────────────────────────────────────────────────

def search(question: str, n_results: int = 2) -> list[str]:
    """Find the most relevant chunks for a question."""
    q_emb   = ollama.embeddings(model=EMBED_MODEL, prompt=question)["embedding"]
    results = collection.query(query_embeddings=[q_emb], n_results=n_results)
    return results["documents"][0]


# ── Step 4: Generate grounded answer ─────────────────────────────────────

def answer(question: str) -> str:
    """Retrieve relevant context and generate a grounded answer."""
    chunks  = search(question)
    context = "\n".join(f"- {c}" for c in chunks)

    prompt = (
        "Answer the question using ONLY the context below.\n"
        'If the answer is not there, say "I don\'t have that information."\n\n'
        f"Context:\n{context}\n\n"
        f"Question: {question}\nAnswer:"
    )
    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


# ── Demo ──────────────────────────────────────────────────────────────────

SAMPLE_DOCS = [
    "Python was created by Guido van Rossum and first released in 1991.",
    "Ollama is an open-source tool for running LLMs locally.",
    "RAG stands for Retrieval-Augmented Generation.",
    "ChromaDB is a lightweight vector database designed for AI applications.",
    "The Llama 3 model family was released by Meta AI in 2024.",
]

QUESTIONS = [
    "Who created Python?",
    "What does RAG stand for?",
    "What is ChromaDB?",
    "What is the capital of Japan?",   # not in context — should say so
]

if __name__ == "__main__":
    index_documents(SAMPLE_DOCS)
    print()
    for q in QUESTIONS:
        print(f"Q: {q}")
        print(f"A: {answer(q)}")
        print("-" * 50)
