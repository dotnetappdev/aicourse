# system_prompts.py — Module 15
"""
Demonstrates the power of system prompts with different personas.

Requirements:
    pip install ollama
    ollama pull llama3.2
"""

import ollama

MODEL = "llama3.2"
QUESTION = "What is a variable?"


def ask_with_system(system: str, question: str) -> str:
    """Ask a question with a custom system prompt."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": question},
        ],
    )
    return response["message"]["content"]


# --- Persona 1: Python Tutor ---
TUTOR_SYSTEM = (
    "You are a concise Python tutor. "
    "Explain things in plain English. "
    "Use short code examples. "
    "Keep answers under 100 words."
)

# --- Persona 2: Pirate ---
PIRATE_SYSTEM = (
    "You are a friendly pirate who teaches programming. "
    "Use pirate slang (arr, matey, ahoy) naturally. "
    "Keep explanations short and use analogies to sailing."
)

# --- Persona 3: ELI5 (Explain Like I'm 5) ---
ELI5_SYSTEM = (
    "Explain everything as if talking to a 5-year-old. "
    "Use very simple words, fun analogies, and short sentences. "
    "Make it friendly and encouraging."
)

PERSONAS = [
    ("Python Tutor", TUTOR_SYSTEM),
    ("Pirate",       PIRATE_SYSTEM),
    ("ELI5",         ELI5_SYSTEM),
]

if __name__ == "__main__":
    for name, system in PERSONAS:
        print(f"\n=== {name} Persona ===")
        print(f"Q: {QUESTION}")
        print(f"A: {ask_with_system(system, QUESTION)}")
        print()
