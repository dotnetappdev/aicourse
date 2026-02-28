# ollama_setup.py — Module 12
"""
Helper script to verify your Ollama installation and list available models.

Usage:
    python ollama_setup.py

Prerequisites:
    pip install ollama
    ollama pull llama3.2
"""

import sys

try:
    import ollama
except ImportError:
    print("ollama package not found. Run: pip install ollama")
    sys.exit(1)


def check_ollama():
    """Check that Ollama is running and list downloaded models."""
    try:
        result = ollama.list()
    except Exception as e:
        print(f"Could not connect to Ollama: {e}")
        print("Make sure Ollama is installed and running.")
        return

    models = result.get("models", [])
    if not models:
        print("Ollama is running but no models are downloaded yet.")
        print("Run: ollama pull llama3.2")
        return

    print(f"Ollama is running. {len(models)} model(s) available:\n")
    print(f"  {'Name':<30} {'Size':>8}")
    print("  " + "-" * 40)
    for m in models:
        size_gb = m["size"] / (1024 ** 3)
        print(f"  {m['name']:<30} {size_gb:>6.1f} GB")


if __name__ == "__main__":
    check_ollama()
