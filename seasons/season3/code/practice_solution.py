"""Season 3 — Practice Project Solution

Enhanced chatbot with /save, /load, and token estimate display.

Usage:
    python practice_solution.py
"""

import json
import os
import ollama

SYSTEM_PROMPT = """You are a friendly and knowledgeable AI assistant.
Keep your answers concise but complete.
If you don't know something, say so honestly."""

HISTORY_FILE = "chat_history.json"
MAX_HISTORY_MESSAGES = 20


def estimate_tokens(text: str) -> int:
    """Rough token estimate: words * 1.3."""
    return int(len(text.split()) * 1.3)


def trim_history(history: list) -> list:
    system_msgs = [m for m in history if m["role"] == "system"]
    other_msgs  = [m for m in history if m["role"] != "system"]
    if len(other_msgs) > MAX_HISTORY_MESSAGES:
        other_msgs = other_msgs[-MAX_HISTORY_MESSAGES:]
    return system_msgs + other_msgs


def save_history(history: list) -> None:
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
    print(f"Conversation saved to {HISTORY_FILE}")


def load_history() -> list:
    if not os.path.exists(HISTORY_FILE):
        print(f"No saved conversation found ({HISTORY_FILE} does not exist).")
        return [{"role": "system", "content": SYSTEM_PROMPT}]
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    print(f"Loaded {len(history)} messages from {HISTORY_FILE}")
    return history


def chat_streaming(messages: list) -> str:
    stream = ollama.chat(model="llama3.2", messages=messages, stream=True)
    print("\nAssistant: ", end="", flush=True)
    full_reply = ""
    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        full_reply += token
    print()
    return full_reply


def print_help():
    print(
        "\nCommands:\n"
        "  /save  — save conversation to file\n"
        "  /load  — load conversation from file\n"
        "  /clear — reset conversation\n"
        "  /help  — show this message\n"
        "  quit   — exit\n"
    )


def main():
    print("AI Chatbot with Save/Load (type /help for commands)")
    print("-" * 55)

    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if user_input.lower() == "/save":
            save_history(history)
            continue

        if user_input.lower() == "/load":
            history = load_history()
            continue

        if user_input.lower() == "/clear":
            history = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Conversation cleared.")
            continue

        if user_input.lower() == "/help":
            print_help()
            continue

        history.append({"role": "user", "content": user_input})
        history = trim_history(history)

        reply = chat_streaming(history)
        history.append({"role": "assistant", "content": reply})

        tokens = estimate_tokens(reply)
        print(f"[tokens: ~{tokens}]")


if __name__ == "__main__":
    main()
