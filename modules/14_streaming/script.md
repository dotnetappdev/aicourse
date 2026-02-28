# Module 14 — Streaming Responses
**~5 min · AI Fundamentals**

---

## Script

**Host:**
By default, `ollama.chat()` waits for the *entire* response before returning — for a long answer that feels slow. **Streaming** sends each token as it's generated, just like ChatGPT's typing effect.

### Basic Streaming

```python
import ollama

stream = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Count from 1 to 10, one per line."}],
    stream=True     # <-- enable streaming
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

print()  # newline after the stream finishes
```

- `end=""` — prevents `print()` adding a newline after each token
- `flush=True` — forces Python to display each token immediately instead of buffering

### Collecting the Full Reply

Often you want to *display* the stream live but also *store* the full reply:

```python
full_reply = ""

for chunk in stream:
    token = chunk["message"]["content"]
    print(token, end="", flush=True)
    full_reply += token

print()
print(f"\n[Total length: {len(full_reply)} chars]")
```

### Detecting the End of the Stream

Each chunk has a `done` field. When `done=True`, the stream is finished and metadata is available:

```python
for chunk in stream:
    if chunk.get("done"):
        tokens = chunk.get("eval_count", 0)
        print(f"\n[Generated {tokens} tokens]")
    else:
        print(chunk["message"]["content"], end="", flush=True)
```

### When to Use Streaming

| Use Case | Recommendation |
|----------|---------------|
| Interactive CLI chatbot | ✅ Always stream |
| Web app with SSE or WebSocket | ✅ Stream |
| Background batch processing | ❌ No streaming needed |
| Short responses < 1 sentence | ❌ Streaming overhead not worth it |

---

## Practice

Modify `qa_bot.py` from Module 13 to stream responses instead of waiting for the full answer.
