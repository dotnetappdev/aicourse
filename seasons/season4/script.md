# Season 4 — Advanced Local LLM Projects
### "RAG, Function Calling, and a Polished CLI App"
**Estimated runtime: ~30 minutes**

---

## Pre-Roll (0:00 – 0:45)

*[Intro music. Course logo.]*

**Host (on camera):**
Welcome to Season 4 — the final season of the core course!

You've come a long way. You can write Python, you understand LLMs, and you can build multi-turn chatbots. This season we're going to apply all of that to three production-level techniques:

1. **RAG** — Retrieval-Augmented Generation: give your LLM access to your own documents
2. **Structured Output** — make the LLM return valid JSON you can use in code
3. **A polished CLI app** — using the `rich` library to make a professional-looking chat interface

Let's do this.

---

## Episode 1 — RAG: Give Your LLM Your Own Documents (0:45 – 12:00)

### What Is RAG? (0:45 – 3:30)

**Host (voiceover):**
LLMs are trained on data up to a certain date. They don't know about your company's internal documents, your personal notes, or anything that happened after their training cutoff.

**RAG — Retrieval-Augmented Generation** — solves this by:

1. **Splitting** your documents into small chunks
2. **Embedding** each chunk into a vector (a list of numbers that captures meaning)
3. **Storing** those vectors in a vector database
4. At query time: **embedding the user's question** and finding the most **similar chunks**
5. **Injecting** those chunks into the prompt as context

The LLM doesn't need to be retrained. It just gets handed the relevant text at runtime.

### Setting Up ChromaDB (3:30 – 6:00)

**Host (voiceover):**
We'll use **ChromaDB** — a lightweight, local vector database — and Ollama's embedding model.

```bash
pip install chromadb ollama
ollama pull nomic-embed-text   # a fast, small embedding model
```

### Building the RAG Pipeline (6:00 – 12:00)

*[Screen share: VS Code with `rag.py`]*

**Host (voiceover):**

```python
import ollama
import chromadb

# ── 1. Initialise the vector store ─────────────────────────────────────────
client     = chromadb.Client()
collection = client.get_or_create_collection("documents")

# ── 2. Add documents ────────────────────────────────────────────────────────
documents = [
    "Python was created by Guido van Rossum in 1991.",
    "Ollama is a tool for running LLMs locally on your own machine.",
    "RAG stands for Retrieval-Augmented Generation.",
    "ChromaDB is a lightweight, open-source vector database.",
    "A large language model predicts the next token in a sequence.",
]

def add_documents(docs: list[str]) -> None:
    embeddings = []
    for doc in docs:
        result = ollama.embeddings(model="nomic-embed-text", prompt=doc)
        embeddings.append(result["embedding"])

    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(docs))]
    )
    print(f"Added {len(docs)} documents to the vector store.")


# ── 3. Query the vector store and generate an answer ────────────────────────
def rag_query(question: str, n_results: int = 2) -> str:
    # Embed the question
    q_embedding = ollama.embeddings(
        model="nomic-embed-text", prompt=question
    )["embedding"]

    # Find the most similar chunks
    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=n_results
    )
    context_chunks = results["documents"][0]

    # Build the prompt with retrieved context
    context = "\n".join(f"- {chunk}" for chunk in context_chunks)
    prompt = f"""Use only the following context to answer the question.
If the answer is not in the context, say "I don't have that information."

Context:
{context}

Question: {question}
Answer:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


if __name__ == "__main__":
    add_documents(documents)
    print(rag_query("Who created Python?"))
    print(rag_query("What does RAG stand for?"))
    print(rag_query("What is the capital of France?"))  # not in context
```

Run it: `python rag.py`

The third question should produce "I don't have that information" — the model correctly limits itself to what's in the context. That's grounded, trustworthy AI.

---

## Episode 2 — Structured Output (JSON Mode) (12:00 – 21:00)

### Why Structured Output? (12:00 – 13:30)

**Host (voiceover):**
Often you don't just want a text reply — you want data you can use in your application. For example: extract product details from a review, classify a support ticket, or generate a list of tasks.

The solution is to ask the model to respond with **JSON** and then parse the output.

### Reliable JSON with a Format Prompt (13:30 – 17:00)

**Host (voiceover):**
The simplest approach: tell the model exactly what JSON structure you want.

```python
import json
import ollama

def extract_product_info(review: str) -> dict:
    """Extract structured product info from a user review."""
    prompt = f"""Extract information from the following product review.
Return ONLY a JSON object with these exact keys:
  - product_name (string)
  - rating (integer 1-5)
  - pros (list of strings)
  - cons (list of strings)
  - would_recommend (boolean)

Review: "{review}"

JSON:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        format="json"   # Ollama's built-in JSON mode
    )

    raw = response["message"]["content"]
    return json.loads(raw)


review = """
I've been using the TechBook Pro laptop for 3 months now.
The battery life is incredible — easily 12 hours — and the keyboard
is a dream to type on. However, the webcam quality is pretty poor
for the price, and the fan gets loud under load. Overall I'd still
recommend it to anyone who values battery life.
"""

info = extract_product_info(review)
print(json.dumps(info, indent=2))
```

The `format="json"` parameter tells Ollama to guarantee valid JSON output — the model will not emit any text outside the JSON object.

### Validating the Output (17:00 – 21:00)

**Host (voiceover):**
Always validate JSON from an LLM — it might be valid JSON but still have the wrong shape.

```python
def validate_product_info(data: dict) -> bool:
    """Basic schema validation."""
    required_keys = {"product_name", "rating", "pros", "cons", "would_recommend"}
    if not required_keys.issubset(data.keys()):
        return False
    if not isinstance(data["rating"], int) or not 1 <= data["rating"] <= 5:
        return False
    if not isinstance(data["pros"], list) or not isinstance(data["cons"], list):
        return False
    return True

if validate_product_info(info):
    print("✅ Valid product info")
else:
    print("❌ Unexpected structure — retrying...")
```

---

## Episode 3 — A Polished CLI App with Rich (21:00 – 27:00)

### Introducing Rich (21:00 – 22:30)

**Host (voiceover):**
The `rich` library turns plain terminal output into beautiful formatted text — markdown rendering, coloured panels, progress bars, tables.

```bash
pip install rich
```

### Building the Rich Chatbot (22:30 – 27:00)

*[Screen share: VS Code with `rich_chat.py`]*

**Host (voiceover):**

```python
import ollama
from rich.console import Console
from rich.panel   import Panel
from rich.prompt  import Prompt
from rich.markdown import Markdown

console = Console()

SYSTEM_PROMPT = """You are a helpful AI assistant.
Format your responses using markdown when appropriate:
use **bold** for emphasis, bullet lists for multiple items,
and code blocks for code."""


def stream_reply(history: list) -> str:
    """Stream the reply, rendering markdown live."""
    stream = ollama.chat(
        model="llama3.2",
        messages=history,
        stream=True
    )

    full_reply = ""
    with console.status("[bold green]Thinking...[/]", spinner="dots"):
        for chunk in stream:
            full_reply += chunk["message"]["content"]

    # Render the complete reply as markdown inside a panel
    console.print(
        Panel(Markdown(full_reply), title="[bold cyan]Assistant[/]", border_style="cyan")
    )
    return full_reply


def main():
    console.print(
        Panel(
            "[bold]Welcome to AI Chat![/]\nType [green]quit[/] to exit.",
            title="[bold magenta]Season 4 — Rich Chatbot[/]",
            border_style="magenta"
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
        reply = stream_reply(history)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
```

Run `python rich_chat.py` and see the difference — it looks like a real application.

---

## Season Wrap-Up (27:00 – 30:00)

*[Host on camera]*

**Host:**
You made it through the entire course! Let's recap everything:

**Season 1 — Python Fundamentals**
Variables, functions, loops, lists, dicts, file I/O

**Season 2 — AI & LLM Fundamentals**
How LLMs work, Ollama setup, first Python chat

**Season 3 — Building with Local LLMs**
Prompt engineering, multi-turn chatbot, context management

**Season 4 — Advanced Projects**
RAG with ChromaDB, structured JSON output, polished CLI with Rich

You now have a complete foundation to build serious, production-quality AI applications — and everything runs **locally**, **privately**, and **for free**.

### Where to Go Next

- Explore more models on **ollama.com/library**
- Try **LangChain** or **LlamaIndex** for more complex pipelines
- Experiment with **function calling** to let your LLM control your application
- Look into **fine-tuning** with tools like **Unsloth** or **MLX**
- Follow the Ollama GitHub repo for new features

Thank you so much for learning with me. Go build something awesome.

*[Outro music]*

---

## 🏋️ Final Capstone Project

Build a **Personal Knowledge Assistant** that:
1. Reads all `.txt` files from a `docs/` folder
2. Splits them into chunks of roughly 200 words
3. Indexes them in ChromaDB
4. Provides a `rich`-powered chat interface
5. Answers questions based only on the indexed documents
6. Shows which document/chunk was used as the source

Sample solution: `code/capstone/`
