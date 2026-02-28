"""Season 3 — Code Examples: Prompt Engineering & Chatbot

Requires:
    pip install ollama
    ollama pull llama3.2
"""

import ollama

# ── Episode 1: System Prompts ──────────────────────────────────────────────

TUTOR_SYSTEM = (
    "You are a helpful Python tutor for beginners. "
    "Always explain things simply. "
    "When you show code, add comments explaining each line. "
    "If the user seems stuck, offer encouragement."
)


def ask_tutor(question: str) -> str:
    """Ask the Python tutor a question and return the answer."""
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": TUTOR_SYSTEM},
            {"role": "user",   "content": question},
        ],
    )
    return response["message"]["content"]


# ── Episode 1: Few-Shot Prompting ──────────────────────────────────────────

def classify_sentiment(review: str) -> str:
    """Classify the sentiment of a review using few-shot prompting."""
    prompt = f"""Classify the sentiment of each review as POSITIVE, NEGATIVE, or NEUTRAL.

Review: "The coffee was amazing!"
Sentiment: POSITIVE

Review: "Waited 20 minutes for cold soup."
Sentiment: NEGATIVE

Review: "The menu has lots of options."
Sentiment: NEUTRAL

Review: "{review}"
Sentiment:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"].strip()


# ── Episode 2: Multi-Turn Chatbot ──────────────────────────────────────────

CHAT_SYSTEM = """You are a friendly and knowledgeable AI assistant.
Keep your answers concise but complete.
If you don't know something, say so honestly."""

MAX_HISTORY_MESSAGES = 20


def trim_history(history: list) -> list:
    """Keep the system prompt and the most recent messages."""
    system_msgs = [m for m in history if m["role"] == "system"]
    other_msgs  = [m for m in history if m["role"] != "system"]
    if len(other_msgs) > MAX_HISTORY_MESSAGES:
        other_msgs = other_msgs[-MAX_HISTORY_MESSAGES:]
    return system_msgs + other_msgs


def chat_streaming(messages: list) -> str:
    """Stream the reply to stdout; return the full text."""
    stream = ollama.chat(model="llama3.2", messages=messages, stream=True)

    print("\nAssistant: ", end="", flush=True)
    full_reply = ""
    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        full_reply += token
    print()
    return full_reply


def run_chatbot():
    """Run the interactive chatbot loop."""
    print("AI Chatbot (type 'quit' to stop, 'clear' to reset)")
    print("-" * 55)

    history = [{"role": "system", "content": CHAT_SYSTEM}]

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if user_input.lower() == "clear":
            history = [{"role": "system", "content": CHAT_SYSTEM}]
            print("Conversation cleared.")
            continue

        history.append({"role": "user", "content": user_input})
        history = trim_history(history)

        reply = chat_streaming(history)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    # Quick demo: tutor + sentiment, then full chatbot
    print("=== Tutor Demo ===")
    print(ask_tutor("What is a for loop?"))

    print("\n=== Sentiment Demo ===")
    print(classify_sentiment("The AI course changed my life!"))

    print("\n=== Chatbot ===")
    run_chatbot()
