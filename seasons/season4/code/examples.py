"""Season 4 — Code Examples: RAG, Structured Output, Rich CLI

Requires:
    pip install ollama chromadb rich
    ollama pull llama3.2
    ollama pull nomic-embed-text
"""

import json
import ollama
import chromadb
from rich.console  import Console
from rich.panel    import Panel
from rich.prompt   import Prompt
from rich.markdown import Markdown

# ── Episode 1: RAG Pipeline ────────────────────────────────────────────────

def build_rag_demo():
    client     = chromadb.Client()
    collection = client.get_or_create_collection("demo_docs")

    documents = [
        "Python was created by Guido van Rossum in 1991.",
        "Ollama is a tool for running LLMs locally on your own machine.",
        "RAG stands for Retrieval-Augmented Generation.",
        "ChromaDB is a lightweight, open-source vector database.",
        "A large language model predicts the next token in a sequence.",
    ]

    # Embed and store each document
    embeddings = [
        ollama.embeddings(model="nomic-embed-text", prompt=doc)["embedding"]
        for doc in documents
    ]
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(documents))],
    )

    def rag_query(question: str, n_results: int = 2) -> str:
        q_emb = ollama.embeddings(model="nomic-embed-text", prompt=question)["embedding"]
        results = collection.query(query_embeddings=[q_emb], n_results=n_results)
        context = "\n".join(f"- {c}" for c in results["documents"][0])

        prompt = (
            "Use only the following context to answer the question.\n"
            "If the answer is not in the context, say \"I don't have that information.\"\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]

    return rag_query


# ── Episode 2: Structured Output ──────────────────────────────────────────

def extract_product_info(review: str) -> dict:
    """Extract structured product info from a user review."""
    prompt = (
        "Extract information from the following product review.\n"
        "Return ONLY a JSON object with these exact keys:\n"
        "  product_name (string), rating (integer 1-5),\n"
        "  pros (list of strings), cons (list of strings),\n"
        "  would_recommend (boolean)\n\n"
        f'Review: "{review}"\n\nJSON:'
    )
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        format="json",
    )
    return json.loads(response["message"]["content"])


# ── Episode 3: Rich CLI Chatbot ────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. "
    "Format responses using markdown when appropriate."
)


def run_rich_chatbot():
    console = Console()

    console.print(
        Panel(
            "[bold]Welcome to AI Chat![/]\nType [green]quit[/] to exit.",
            title="[bold magenta]Season 4 — Rich Chatbot[/]",
            border_style="magenta",
        )
    )

    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = Prompt.ask("\n[bold yellow]You[/]").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            console.print("[bold red]Goodbye![/]")
            break

        history.append({"role": "user", "content": user_input})

        stream = ollama.chat(model="llama3.2", messages=history, stream=True)
        full_reply = ""
        with console.status("[bold green]Thinking...[/]", spinner="dots"):
            for chunk in stream:
                full_reply += chunk["message"]["content"]

        console.print(
            Panel(
                Markdown(full_reply),
                title="[bold cyan]Assistant[/]",
                border_style="cyan",
            )
        )
        history.append({"role": "assistant", "content": full_reply})


if __name__ == "__main__":
    # RAG demo
    print("=== RAG Demo ===")
    query = build_rag_demo()
    print(query("Who created Python?"))
    print(query("What does RAG stand for?"))
    print(query("What is the capital of France?"))

    # Structured output demo
    print("\n=== Structured Output Demo ===")
    review = (
        "I've been using the TechBook Pro for 3 months. "
        "Battery life is incredible — 12 hours easily — and the keyboard feels great. "
        "The webcam quality is poor and the fan gets loud. I'd still recommend it."
    )
    info = extract_product_info(review)
    print(json.dumps(info, indent=2))

    # Rich chatbot
    print("\n=== Rich Chatbot ===")
    run_rich_chatbot()
