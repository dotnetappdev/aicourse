# Module 17 — Multi-Turn Chatbot
**~7 min · Prompt Engineering**

---

## Script

**Host:**
Here's a fact that surprises beginners: **LLMs have no memory**. Every call to `ollama.chat()` is completely independent — the model has forgotten everything you said before.

The trick? Send the **entire conversation history** with every request. Your Python code is the memory. Let's build a proper chatbot.

### The Conversation History

The `messages` list we've been using is the conversation. If we keep adding to it and resend it each time, the model can "remember":

```python
history = [
    {"role": "system",    "content": "You are a helpful assistant."},
    {"role": "user",      "content": "My name is Alice."},
    {"role": "assistant", "content": "Hi Alice! How can I help?"},
    {"role": "user",      "content": "What is my name?"},   # <-- new message
]

# The model will answer "Alice" because the full history is included
```

### Building the Chatbot Loop

```python
import ollama

SYSTEM = "You are a friendly and helpful AI assistant."

history = [{"role": "system", "content": SYSTEM}]

print("Chatbot (type 'quit' to exit)\n")

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # 1. Add user message to history
    history.append({"role": "user", "content": user_input})

    # 2. Send full history, get reply
    response = ollama.chat(model="llama3.2", messages=history)
    reply = response["message"]["content"]

    # 3. Add assistant reply to history
    history.append({"role": "assistant", "content": reply})

    print(f"\nAssistant: {reply}\n")
```

### Adding Streaming

Replace the `ollama.chat()` call with streaming for a better experience:

```python
stream = ollama.chat(model="llama3.2", messages=history, stream=True)

reply = ""
print("\nAssistant: ", end="", flush=True)
for chunk in stream:
    token = chunk["message"]["content"]
    print(token, end="", flush=True)
    reply += token
print()

history.append({"role": "assistant", "content": reply})
```

### Adding a /clear Command

```python
if user_input.lower() == "/clear":
    history = [{"role": "system", "content": SYSTEM}]
    print("Conversation cleared.\n")
    continue
```

---

## Practice

Add a `/history` command to the chatbot that prints all messages in the conversation so far (excluding the system message).
