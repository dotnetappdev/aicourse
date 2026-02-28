# streaming.py — Module 14
"""
Demonstrates streaming responses from a local Ollama model.

Requirements:
    pip install ollama
    ollama pull llama3.2
"""

import ollama

MODEL = "llama3.2"


def stream_basic():
    """Stream tokens to the terminal as they are generated."""
    print("--- Basic Streaming ---")
    stream = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": "Count from 1 to 5, one per line."}],
        stream=True,
    )
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)
    print()


def stream_with_collection():
    """Stream and collect the full reply at the same time."""
    print("\n--- Stream + Collect ---")
    stream = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": "Name three programming languages."}],
        stream=True,
    )
    full_reply = ""
    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        full_reply += token
    print()
    print(f"[Total length: {len(full_reply)} chars]")


def stream_with_metadata():
    """Stream and show token count when done."""
    print("\n--- Stream + Metadata ---")
    stream = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": "What is RAG in one sentence?"}],
        stream=True,
    )
    for chunk in stream:
        if chunk.get("done"):
            tokens = chunk.get("eval_count", 0)
            print(f"\n[Generated {tokens} tokens]")
        else:
            print(chunk["message"]["content"], end="", flush=True)


if __name__ == "__main__":
    stream_basic()
    stream_with_collection()
    stream_with_metadata()
