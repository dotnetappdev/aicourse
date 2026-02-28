# context_management.py — Module 18
"""
Strategies for managing conversation history length.

Requirements:
    pip install ollama
    ollama pull llama3.2
"""

import ollama

MODEL = "llama3.2"


# ── Helpers ───────────────────────────────────────────────────────────────

def estimate_tokens(messages: list) -> int:
    """Rough token estimate (chars / 4)."""
    return sum(len(m["content"]) for m in messages) // 4


# ── Strategy 1: Keep last N turns ─────────────────────────────────────────

def trim_history(history: list, max_turns: int = 10) -> list:
    """Keep the system prompt and the most recent `max_turns` messages."""
    system = [m for m in history if m["role"] == "system"]
    other  = [m for m in history if m["role"] != "system"]
    if len(other) > max_turns:
        other = other[-max_turns:]
    return system + other


# ── Strategy 2: Summarise old turns ───────────────────────────────────────

def summarise_history(history: list) -> list:
    """Replace old turns with a brief summary, keeping the last 2 turns."""
    system = [m for m in history if m["role"] == "system"]
    other  = [m for m in history if m["role"] != "system"]

    if len(other) <= 4:
        return history  # not long enough to need summarising

    to_summarise = other[:-2]
    recent       = other[-2:]

    text = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in to_summarise)
    summary_resp = ollama.chat(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": f"Summarise this conversation in 3 sentences:\n\n{text}"
        }],
    )
    summary = summary_resp["message"]["content"]

    return system + [{"role": "system", "content": f"Earlier summary: {summary}"}] + recent


# ── Demo chatbot with trimming + token display ────────────────────────────

def main():
    SYSTEM  = "You are a helpful AI assistant."
    history = [{"role": "system", "content": SYSTEM}]

    print("Chatbot with context management (type 'quit' to exit)\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            break

        history.append({"role": "user", "content": user_input})
        history = trim_history(history, max_turns=10)

        stream = ollama.chat(model=MODEL, messages=history, stream=True)
        reply  = ""
        print("\nAssistant: ", end="", flush=True)
        for chunk in stream:
            token = chunk["message"]["content"]
            print(token, end="", flush=True)
            reply += token
        print()

        history.append({"role": "assistant", "content": reply})

        tokens = estimate_tokens(history)
        print(f"[~{tokens} tokens in context | {len(history) - 1} messages]\n")


if __name__ == "__main__":
    main()
