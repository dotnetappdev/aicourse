# prompt_techniques.py — Module 16
"""
Five prompt engineering techniques in action.

Requirements:
    pip install ollama
    ollama pull llama3.2
"""

import ollama

MODEL = "llama3.2"


def ask(prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    return ollama.chat(model=MODEL, messages=messages)["message"]["content"]


# ── 1. Be Specific ─────────────────────────────────────────────────────────
specific_prompt = """Write a Python function called `word_count` that:
- Takes a string as input
- Returns a dictionary: keys=words, values=occurrence counts
- Is case-insensitive
- Ignores punctuation
Include a docstring and 2 usage examples."""

print("=== 1. Specific Prompt ===")
print(ask(specific_prompt))


# ── 2. Few-Shot Prompting ─────────────────────────────────────────────────
few_shot_prompt = """Classify the sentiment as POSITIVE, NEGATIVE, or NEUTRAL.

Review: "The coffee was amazing!"
Sentiment: POSITIVE

Review: "Waited 20 minutes for cold soup."
Sentiment: NEGATIVE

Review: "The menu has lots of options."
Sentiment: NEUTRAL

Review: "The AI course changed my life!"
Sentiment:"""

print("\n=== 2. Few-Shot ===")
print(ask(few_shot_prompt))


# ── 3. Chain of Thought ───────────────────────────────────────────────────
cot_prompt = """A store has 50 apples. They sell 3 bags of 6 apples each,
then receive a delivery of 20 apples. How many apples do they have?

Think through this step by step before giving your final answer."""

print("\n=== 3. Chain of Thought ===")
print(ask(cot_prompt))


# ── 4. Structured Output ──────────────────────────────────────────────────
format_prompt = """List the top 3 reasons to use Python for AI development.
Format as a numbered list. Each item: bold title + one-sentence explanation.
Example:
1. **Title**: Explanation here."""

print("\n=== 4. Structured Output ===")
print(ask(format_prompt))


# ── 5. Role Prompting ─────────────────────────────────────────────────────
review_system = (
    "You are a senior Python code reviewer. "
    "Focus on correctness, readability, and Pythonic style. "
    "Be concise and specific."
)
review_prompt = """Review this function and suggest one improvement:

def calc(x,y):
    return x+y"""

print("\n=== 5. Role Prompting ===")
print(ask(review_prompt, system=review_system))
