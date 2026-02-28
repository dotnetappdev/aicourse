# chatbot.py — Module 17
"""
Multi-turn chatbot that maintains full conversation history.

Commands:
    /clear   — reset the conversation
    /history — show all messages so far
    quit     — exit

Requirements:
    pip install ollama
    ollama pull llama3.2
"""

import ollama

MODEL  = "llama3.2"
SYSTEM = "You are a friendly and helpful AI assistant."


def stream_reply(messages: list) -> str:
    """Stream a reply and return the full text."""
    stream = ollama.chat(model=MODEL, messages=messages, stream=True)
    reply = ""
    print("\nAssistant: ", end="", flush=True)
    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        reply += token
    print()
    return reply


def show_history(history: list) -> None:
    """Print conversation history (excluding the system message)."""
    turns = [m for m in history if m["role"] != "system"]
    if not turns:
        print("No conversation yet.")
        return
    for msg in turns:
        role = "You" if msg["role"] == "user" else "Assistant"
        print(f"  [{role}] {msg['content'][:80]}{'...' if len(msg['content']) > 80 else ''}")


def main():
    history = [{"role": "system", "content": SYSTEM}]
    print("Chatbot — /clear to reset, /history to review, 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if user_input.lower() == "/clear":
            history = [{"role": "system", "content": SYSTEM}]
            print("Conversation cleared.\n")
            continue

        if user_input.lower() == "/history":
            show_history(history)
            continue

        history.append({"role": "user", "content": user_input})
        reply = stream_reply(history)
        history.append({"role": "assistant", "content": reply})
        print()


if __name__ == "__main__":
    main()
