# Module 19 — RAG: Retrieval-Augmented Generation
**~8 min · Advanced Projects**

---

## Script

**Host:**
LLMs are trained on public data up to a cutoff date. They don't know about your company's internal documents, your personal notes, or anything recent. **RAG** solves this.

### What Is RAG?

RAG stands for **Retrieval-Augmented Generation**. The pipeline:

1. **Split** your documents into small chunks (~200 words each)
2. **Embed** each chunk into a vector (a list of numbers representing its meaning)
3. **Store** those vectors in a vector database
4. **Query**: embed the user's question, find the most similar chunks
5. **Generate**: give the LLM those chunks as context to answer the question

```
User question
     │
     ▼
 [Embed question] → vector search → [Top 3 chunks]
                                          │
                                          ▼
                               prompt = context + question
                                          │
                                          ▼
                                      [LLM answer]
```

### Setup

```bash
pip install ollama chromadb
ollama pull nomic-embed-text   # fast, small embedding model (~274 MB)
```

### Building the RAG Pipeline

**Step 1 — Embedding and storing documents:**

```python
import ollama
import chromadb

client     = chromadb.Client()
collection = client.get_or_create_collection("my_docs")

documents = [
    "Python was created by Guido van Rossum and released in 1991.",
    "Ollama is a tool for running LLMs locally on your own machine.",
    "RAG stands for Retrieval-Augmented Generation.",
    "ChromaDB is a lightweight vector database for AI applications.",
]

for i, doc in enumerate(documents):
    embedding = ollama.embeddings(model="nomic-embed-text", prompt=doc)["embedding"]
    collection.add(documents=[doc], embeddings=[embedding], ids=[f"doc_{i}"])

print(f"Indexed {len(documents)} documents.")
```

**Step 2 — Querying:**

```python
def search(question: str, n: int = 2) -> list[str]:
    q_emb = ollama.embeddings(model="nomic-embed-text", prompt=question)["embedding"]
    results = collection.query(query_embeddings=[q_emb], n_results=n)
    return results["documents"][0]


def answer(question: str) -> str:
    chunks  = search(question)
    context = "\n".join(f"- {c}" for c in chunks)

    prompt = (
        "Answer the question using ONLY the context below.\n"
        'If the answer is not there, say "I don\'t have that information."\n\n'
        f"Context:\n{context}\n\n"
        f"Question: {question}\nAnswer:"
    )
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


print(answer("Who made Python?"))
print(answer("What is the capital of Japan?"))  # not in context
```

### Why This Works

The model only ever sees the chunks you retrieved. It can't hallucinate facts from outside that context — you've grounded it to your documents.

---

## Practice

Create `rag_from_files.py` that reads `.txt` files from a `docs/` folder, indexes them, and answers questions about them.
