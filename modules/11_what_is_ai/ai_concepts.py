# ai_concepts.py — Module 11
# Demonstrates AI terminology in code comments

# A "model" in machine learning is a function that maps input -> output.
# We represent it symbolically here (real LLMs are run with Ollama).

def simple_model(input_text: str) -> str:
    """
    Toy model: very basic rule-based 'AI'.
    Real LLMs use billions of parameters instead of these rules.
    """
    input_lower = input_text.lower()
    if "hello" in input_lower:
        return "Hi there!"
    if "how are you" in input_lower:
        return "I'm doing great, thanks for asking!"
    return "I don't understand that yet."


# "Inference" = running the model to get a prediction
responses = [
    simple_model("Hello!"),
    simple_model("How are you today?"),
    simple_model("What is a transformer?"),
]

for r in responses:
    print(r)


# Tokens: split text into rough token-sized pieces
def count_tokens(text: str) -> int:
    """Rough token estimate: words × 1.3."""
    return int(len(text.split()) * 1.3)


sentence = "Python is a great language for AI development."
print(f"'{sentence}' ≈ {count_tokens(sentence)} tokens")


# Quiz practice project
QUESTIONS = [
    {
        "question": "What does LLM stand for?",
        "options": ["A) Large Learning Module", "B) Large Language Model",
                    "C) Linear Logic Machine"],
        "answer": "B",
    },
    {
        "question": "What is inference?",
        "options": ["A) Training the model", "B) Updating weights",
                    "C) Running the model to get output"],
        "answer": "C",
    },
    {
        "question": "What is quantisation?",
        "options": ["A) Compressing a model to use less memory",
                    "B) Training with more data",
                    "C) Adding more parameters"],
        "answer": "A",
    },
]


def run_quiz(questions: list) -> None:
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['question']}")
        for opt in q["options"]:
            print(f"  {opt}")
        answer = input("Your answer (A/B/C): ").strip().upper()
        if answer == q["answer"]:
            print("✓ Correct!")
            score += 1
        else:
            print(f"✗ The answer was {q['answer']}.")
    print(f"\nYou scored {score}/{len(questions)}")


if __name__ == "__main__":
    run_quiz(QUESTIONS)
