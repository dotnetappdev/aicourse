# Module 13 — First Python Chat with Ollama
**~6 min · AI Fundamentals**

---

## Script

**Host:**
Time to write Python code that actually talks to an LLM. Install the Ollama Python library:

```bash
pip install ollama
```

### Your First Chat

Create `first_chat.py`:

```python
import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "What is Python?"}
    ]
)

print(response["message"]["content"])
```

Run it. You'll see the model's answer in your terminal.

### The Message Format

Every message is a dictionary with two keys:

```python
{"role": "user",      "content": "Your message here"}
{"role": "assistant", "content": "The model's reply"}
{"role": "system",    "content": "Instructions for the model"}
```

This format is the **OpenAI chat standard** — virtually every LLM API in the world uses it.

### What Does `response` Look Like?

```python
import json

response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Say hi!"}]
)

# See the full response structure
print(json.dumps(dict(response), indent=2, default=str))
```

Key fields:
- `response["message"]["content"]` — the actual reply text
- `response["model"]` — which model replied
- `response["done"]` — whether generation is complete
- `response["eval_count"]` — tokens generated

### Asking Multiple Questions

```python
questions = [
    "What is a variable in Python?",
    "What is a function?",
    "What is a list?",
]

for question in questions:
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": question}]
    )
    print(f"Q: {question}")
    print(f"A: {response['message']['content']}")
    print("-" * 40)
```

---

## Practice

Write `qa_bot.py` that takes a question from the user via `input()`, asks llama3.2, and prints the answer.
