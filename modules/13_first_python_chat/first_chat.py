# first_chat.py — Module 13
"""
Your first Python chat with a local LLM via Ollama.

Requirements:
    pip install ollama
    ollama pull llama3.2
"""

import ollama

# --- Single question ---
response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "What is Python?"}
    ],
)

print(response["message"]["content"])
print()

# --- Inspect the full response ---
print("Model:", response["model"])
print("Tokens generated:", response.get("eval_count", "N/A"))
print()

# --- Ask multiple questions ---
questions = [
    "What is a variable in Python?",
    "What is a function?",
    "What is a list?",
]

for question in questions:
    resp = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": question}],
    )
    print(f"Q: {question}")
    print(f"A: {resp['message']['content']}")
    print("-" * 40)
