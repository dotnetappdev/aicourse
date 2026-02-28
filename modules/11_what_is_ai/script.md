# Module 11 — What Is AI, ML & LLMs?
**~7 min · AI Fundamentals**

---

## Script

**Host:**
Now that you know Python, let's understand *what* you're actually building with. Today: a plain-English explanation of AI, machine learning, and large language models.

### The Three Circles

Think of it like nested circles:

```
┌─────────────────────────────────────┐
│  Artificial Intelligence            │
│  ┌───────────────────────────────┐  │
│  │  Machine Learning             │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  Deep Learning / LLMs   │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Artificial Intelligence** is the broad field of making computers do things that normally require human intelligence.

**Machine Learning** is the approach where computers *learn from data* rather than following hand-coded rules.

**LLMs** (Large Language Models) are a specific type of deep learning model trained on text to understand and generate human language.

### How an LLM Actually Works

1. **Training**: The model reads billions of text examples and adjusts its internal numbers (called *weights* or *parameters*) to predict what word comes next.

2. **Inference**: You give it a prompt. It predicts the next token. Then the next. Then the next. That's the entire mechanism.

3. **Scale**: The "Large" in LLM matters — a 70-billion-parameter model has 70 billion numbers all tuned together. This is why they're so capable.

### Key Vocabulary

| Term | Definition |
|------|-----------|
| **Model** | The trained system (e.g., llama3, mistral) |
| **Parameters / weights** | The numbers the model learned — "8B" = 8 billion |
| **Token** | A piece of text (~4 characters on average) |
| **Context window** | How many tokens the model can read at once |
| **Prompt** | Text you send as input |
| **Inference** | Running the model to get output |
| **Quantisation** | Compressing the model (Q4 = 4-bit, smaller file) |

### Why Run Locally?

Running models on your own machine (vs. a cloud API) gives you:

- ✅ **Privacy** — your data never leaves your computer
- ✅ **No cost** — no API charges
- ✅ **No rate limits** — run as many requests as you want
- ✅ **Offline** — works without internet
- ⚠️ **Requires RAM** — ~4 GB for 3B models, ~8 GB for 7B models

---

## Practice

Write `ai_quiz.py` that asks the user 3 multiple-choice questions about AI terminology and prints their score.
