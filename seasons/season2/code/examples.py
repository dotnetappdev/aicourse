"""Season 2 — Code Examples: AI & LLM Fundamentals

Requires:
    pip install ollama
    ollama pull llama3.2
"""

import ollama


# ── Episode 3: Basic Chat ──────────────────────────────────────────────────

def basic_chat():
    """Send a single message and print the full response."""
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": "What is a large language model?"}
        ],
    )
    print(response["message"]["content"])


# ── Episode 3: Streaming Response ─────────────────────────────────────────

def streaming_chat():
    """Stream the response token by token."""
    stream = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "user", "content": "Explain Python in 3 sentences."}
        ],
        stream=True,
    )

    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)
    print()


# ── Bonus: List available models ───────────────────────────────────────────

def list_models():
    """Print all locally available Ollama models."""
    models = ollama.list()
    print("Available models:")
    for model in models["models"]:
        # Size is in bytes; convert to GB for readability
        size_gb = model["size"] / (1024 ** 3)
        print(f"  {model['name']:<30} {size_gb:.1f} GB")


if __name__ == "__main__":
    list_models()
    print("\n--- Basic Chat ---")
    basic_chat()
    print("\n--- Streaming Chat ---")
    streaming_chat()
