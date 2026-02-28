"""Season 2 — Practice Project Solution

Lists available Ollama models, lets the user pick one,
then streams an answer to their question.

Usage:
    python practice_solution.py
"""

import ollama


def format_size(bytes_: int) -> str:
    """Convert bytes to a human-readable string."""
    gb = bytes_ / (1024 ** 3)
    if gb >= 1:
        return f"{gb:.1f} GB"
    mb = bytes_ / (1024 ** 2)
    return f"{mb:.0f} MB"


def main():
    # 1. List downloaded models
    result = ollama.list()
    models = result.get("models", [])

    if not models:
        print("No models found. Run: ollama pull llama3.2")
        return

    print("Available models:")
    print(f"  {'#':<4} {'Name':<30} {'Size'}")
    print("  " + "-" * 45)
    for i, model in enumerate(models):
        size = format_size(model["size"])
        print(f"  {i + 1:<4} {model['name']:<30} {size}")

    # 2. Ask the user which model to use
    while True:
        raw = input("\nEnter the number of the model to use: ")
        if raw.isdigit() and 1 <= int(raw) <= len(models):
            chosen = models[int(raw) - 1]["name"]
            break
        print(f"Please enter a number between 1 and {len(models)}.")

    # 3. Ask for a question
    question = input(f"\nWhat do you want to ask {chosen}?\n> ")

    # 4. Stream the response
    print(f"\n{chosen}: ", end="", flush=True)
    stream = ollama.chat(
        model=chosen,
        messages=[{"role": "user", "content": question}],
        stream=True,
    )
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)
    print()


if __name__ == "__main__":
    main()
