"""
Season 4 — Capstone Project: Personal Knowledge Assistant

Indexes all .txt files in the docs/ folder, then answers questions
using RAG with a rich-formatted chat interface.

Usage:
    1. Put your .txt files in the docs/ folder.
    2. Run: python assistant.py
"""

import os
import glob
import ollama
import chromadb
from rich.console  import Console
from rich.panel    import Panel
from rich.prompt   import Prompt
from rich.markdown import Markdown
from rich.table    import Table


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

DOCS_FOLDER     = os.path.join(os.path.dirname(__file__), "docs")
EMBED_MODEL     = "nomic-embed-text"
CHAT_MODEL      = "llama3.2"
CHUNK_SIZE      = 200   # approximate words per chunk
N_RESULTS       = 3     # chunks to retrieve per query
COLLECTION_NAME = "knowledge_base"

console = Console()


# ─────────────────────────────────────────────────────────────────────────────
# Document helpers
# ─────────────────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """Split text into chunks of approximately chunk_size words."""
    words  = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks


def load_documents(folder: str) -> list[dict]:
    """Read all .txt files from folder and return list of {source, text} dicts."""
    docs = []
    for path in glob.glob(os.path.join(folder, "*.txt")):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        if text:
            docs.append({"source": os.path.basename(path), "text": text})
    return docs


# ─────────────────────────────────────────────────────────────────────────────
# Vector store
# ─────────────────────────────────────────────────────────────────────────────

def build_index(collection, docs: list[dict]) -> int:
    """Chunk, embed, and index all documents. Returns total chunk count."""
    all_texts, all_ids, all_metas, all_embeddings = [], [], [], []
    chunk_id = 0

    with console.status("[bold green]Indexing documents...[/]", spinner="dots"):
        for doc in docs:
            chunks = chunk_text(doc["text"])
            for i, chunk in enumerate(chunks):
                embedding = ollama.embeddings(
                    model=EMBED_MODEL, prompt=chunk
                )["embedding"]
                all_texts.append(chunk)
                all_ids.append(f"chunk_{chunk_id}")
                all_metas.append({"source": doc["source"], "chunk_index": i})
                all_embeddings.append(embedding)
                chunk_id += 1

    if all_ids:
        collection.add(
            documents=all_texts,
            embeddings=all_embeddings,
            ids=all_ids,
            metadatas=all_metas,
        )
    return chunk_id


def retrieve(collection, question: str, n: int = N_RESULTS) -> list[dict]:
    """Return the top-n most relevant chunks for the question."""
    q_emb = ollama.embeddings(model=EMBED_MODEL, prompt=question)["embedding"]
    results = collection.query(query_embeddings=[q_emb], n_results=n)
    chunks = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({"text": text, "source": meta["source"],
                       "chunk": meta["chunk_index"]})
    return chunks


# ─────────────────────────────────────────────────────────────────────────────
# RAG answer generation
# ─────────────────────────────────────────────────────────────────────────────

def generate_answer(question: str, chunks: list[dict]) -> str:
    """Generate a grounded answer using retrieved chunks."""
    context_lines = [
        f'[From "{c["source"]}", chunk {c["chunk"]}]: {c["text"]}'
        for c in chunks
    ]
    context = "\n\n".join(context_lines)

    prompt = (
        "You are a knowledge assistant. Answer the question using ONLY the context below.\n"
        "If the answer cannot be found in the context, say exactly: "
        "\"I don't have that information in my documents.\"\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer (use markdown formatting):"
    )

    stream = ollama.chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    full_reply = ""
    with console.status("[bold green]Thinking...[/]", spinner="dots"):
        for chunk in stream:
            full_reply += chunk["message"]["content"]
    return full_reply


# ─────────────────────────────────────────────────────────────────────────────
# Main application
# ─────────────────────────────────────────────────────────────────────────────

def print_sources(chunks: list[dict]) -> None:
    table = Table(title="Sources Used", show_header=True, header_style="bold dim")
    table.add_column("File", style="cyan")
    table.add_column("Chunk #", justify="right")
    table.add_column("Preview", no_wrap=False, max_width=60)
    for c in chunks:
        preview = c["text"][:80] + "..." if len(c["text"]) > 80 else c["text"]
        table.add_row(c["source"], str(c["chunk"]), preview)
    console.print(table)


def main():
    # ── Startup ──────────────────────────────────────────────────────────────
    console.print(
        Panel(
            "[bold]Personal Knowledge Assistant[/]\n"
            f"Documents folder: [cyan]{DOCS_FOLDER}[/]\n"
            "Type [green]quit[/] to exit.",
            title="[bold magenta]Season 4 — Capstone[/]",
            border_style="magenta",
        )
    )

    # ── Load documents ────────────────────────────────────────────────────────
    docs = load_documents(DOCS_FOLDER)
    if not docs:
        console.print(
            f"[bold red]No .txt files found in {DOCS_FOLDER}.[/]\n"
            "Add some text files and try again."
        )
        return

    console.print(f"Found [bold]{len(docs)}[/] document(s): "
                  + ", ".join(d["source"] for d in docs))

    # ── Build vector index ────────────────────────────────────────────────────
    db_client  = chromadb.Client()
    collection = db_client.get_or_create_collection(COLLECTION_NAME)
    n_chunks   = build_index(collection, docs)
    console.print(f"Indexed [bold]{n_chunks}[/] chunks. Ready!\n")

    # ── Chat loop ─────────────────────────────────────────────────────────────
    while True:
        question = Prompt.ask("[bold yellow]Ask a question[/]").strip()

        if not question:
            continue
        if question.lower() in ("quit", "exit"):
            console.print("[bold red]Goodbye![/]")
            break

        chunks = retrieve(collection, question)
        answer = generate_answer(question, chunks)

        console.print(
            Panel(
                Markdown(answer),
                title="[bold cyan]Answer[/]",
                border_style="cyan",
            )
        )
        print_sources(chunks)


if __name__ == "__main__":
    main()
