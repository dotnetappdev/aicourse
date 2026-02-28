# Module 18 — Context Management
**~5 min · Prompt Engineering**

---

## Script

**Host:**
The **context window** is the maximum amount of text an LLM can process at once. For Llama 3.2, that's 128,000 tokens — very large. But in a very long conversation, you can approach that limit, and performance can degrade.

This module covers how to manage your conversation history responsibly.

### Estimating Token Usage

A rough estimate: 1 token ≈ 4 characters or ¾ of a word.

```python
def estimate_tokens(messages: list) -> int:
    """Rough token estimate for a list of messages."""
    total_chars = sum(len(m["content"]) for m in messages)
    return total_chars // 4
```

### Strategy 1 — Keep Last N Turns

The simplest approach: discard old messages once the history gets long.

```python
MAX_TURNS = 10   # keep system + last 10 turns

def trim_history(history: list, max_turns: int = MAX_TURNS) -> list:
    """Keep the system prompt and the most recent turns."""
    system = [m for m in history if m["role"] == "system"]
    other  = [m for m in history if m["role"] != "system"]

    if len(other) > max_turns:
        other = other[-max_turns:]

    return system + other
```

Use it before every chat call:

```python
history = trim_history(history)
response = ollama.chat(model="llama3.2", messages=history)
```

### Strategy 2 — Summarise Old Turns

Instead of discarding, summarise:

```python
def summarise_history(history: list, model: str = "llama3.2") -> list:
    """
    Summarise all non-system turns into a single context message.
    Returns a new history with: system + summary + last 2 turns.
    """
    import ollama

    system = [m for m in history if m["role"] == "system"]
    other  = [m for m in history if m["role"] != "system"]

    if len(other) <= 4:
        return history  # not long enough to need summarising

    to_summarise = other[:-2]   # everything except the last 2 turns
    recent       = other[-2:]

    conversation_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in to_summarise
    )

    summary_response = ollama.chat(
        model=model,
        messages=[{
            "role": "user",
            "content": f"Summarise this conversation in 3 sentences:\n\n{conversation_text}"
        }]
    )
    summary = summary_response["message"]["content"]

    summary_message = {
        "role": "system",
        "content": f"Earlier conversation summary: {summary}"
    }

    return system + [summary_message] + recent
```

### Which Strategy to Use?

| Strategy | When | Trade-off |
|----------|------|-----------|
| Trim (keep last N) | Most chatbots | May lose earlier context |
| Summarise | Long-running assistants | Costs extra tokens to summarise |
| Full history | Short conversations | Fine until context limit is hit |

---

## Practice

Add a token usage display to `chatbot.py`: after each reply, print `[~N tokens in context]` using the `estimate_tokens()` function.
