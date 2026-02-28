# qa_bot.py — Module 13 Practice
"""
Simple Q&A bot: takes a question from the user and answers it.

Usage:
    python qa_bot.py
"""

import ollama


def ask(question: str, model: str = "llama3.2") -> str:
    """Ask the model a single question and return the answer."""
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": question}],
    )
    return response["message"]["content"]


def main():
    print("Q&A Bot — type 'quit' to exit\n")
    while True:
        question = input("Your question: ").strip()
        if not question:
            continue
        if question.lower() in ("quit", "exit"):
            break
        answer = ask(question)
        print(f"\nAnswer: {answer}\n")


if __name__ == "__main__":
    main()
