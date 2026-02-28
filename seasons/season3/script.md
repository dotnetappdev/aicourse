# Season 3 — Building with Local LLMs
### "Prompt Engineering and Building a Memory-Aware Chatbot"
**Estimated runtime: ~30 minutes**

---

## Pre-Roll (0:00 – 0:45)

*[Intro music. Course logo.]*

**Host (on camera):**
Season 3! You now know Python and you can talk to a local LLM from code. Today we level up.

We're going to cover **prompt engineering** — the art of writing instructions that get the best results from LLMs — and then we'll build a proper **command-line chatbot** that keeps track of the full conversation history, just like ChatGPT does.

This is where things start to feel like real AI development. Let's go.

---

## Episode 1 — Prompt Engineering Basics (0:45 – 12:00)

### What Is a Prompt? (0:45 – 2:30)

**Host (voiceover):**
A **prompt** is the text you send to the model. Everything the model knows about what you want comes from your prompt. Writing good prompts is arguably the most important skill in applied AI development.

The chat API uses three message roles:

| Role | Purpose |
|------|---------|
| `system` | Sets the model's persona and rules (sent once at the start) |
| `user` | What you say |
| `assistant` | What the model says |

### System Prompts (2:30 – 5:30)

**Host (voiceover):**
The **system prompt** is the most powerful part of your prompt. It tells the model *who it is* and *how it should behave*.

```python
import ollama

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful Python tutor for beginners. "
            "Always explain things simply. "
            "When you show code, add comments explaining each line. "
            "If the user seems stuck, offer encouragement."
        )
    },
    {
        "role": "user",
        "content": "What is a for loop?"
    }
]

response = ollama.chat(model="llama3.2", messages=messages)
print(response["message"]["content"])
```

Compare this to asking the same question without a system prompt — the tutor persona makes the answer much more appropriate for beginners.

### Prompt Engineering Techniques (5:30 – 12:00)

**Host (voiceover):**
Here are the most useful techniques, in order of how often you'll use them:

#### 1. Be Specific

Bad:
```
Write code.
```

Good:
```
Write a Python function called `count_words` that takes a string and 
returns a dictionary where each key is a word and the value is how 
many times that word appears. Use only the Python standard library.
```

#### 2. Give Examples (Few-Shot Prompting)

Showing the model examples of what you want is often more effective than describing it.

```python
prompt = """
Classify the sentiment of each review as POSITIVE, NEGATIVE, or NEUTRAL.

Review: "The coffee was amazing!"
Sentiment: POSITIVE

Review: "Waited 20 minutes for cold soup."
Sentiment: NEGATIVE

Review: "The menu has lots of options."
Sentiment: NEUTRAL

Review: "The AI course changed my life!"
Sentiment:"""
```

#### 3. Chain of Thought

For reasoning tasks, ask the model to think step by step:

```python
prompt = """
A store sells apples for $0.50 each and bananas for $0.30 each. 
Alice buys 4 apples and 3 bananas. How much does she pay in total?

Think step by step before giving your final answer.
"""
```

#### 4. Output Formatting

Tell the model exactly what format you want:

```python
prompt = """
List the top 3 benefits of using local LLMs.
Respond in JSON with this exact structure:
{
  "benefits": [
    {"title": "...", "description": "..."},
    ...
  ]
}
Only output the JSON, nothing else.
"""
```

#### 5. Role Prompting

```python
system = """
You are an expert senior Python developer with 15 years of experience.
Review the user's code and provide detailed, constructive feedback 
focused on correctness, readability, and Pythonic style.
"""
```

---

## Episode 2 — Building a Multi-Turn Chatbot (12:00 – 24:00)

### Why Conversation History Matters (12:00 – 14:00)

**Host (voiceover):**
Here's something crucial: **LLMs have no memory between calls**. Every time you call `ollama.chat()`, the model starts completely fresh — it has no idea what you said before.

The way to give an LLM "memory" is simple: send the entire conversation history with every request. That's what ChatGPT does under the hood. Your client (the Python code) keeps a list of all messages and sends the full list every time.

### The Chatbot Code (14:00 – 24:00)

*[Screen share: VS Code with `chatbot.py`]*

**Host (voiceover):**
Let's build it. Create `chatbot.py`:

```python
import ollama

SYSTEM_PROMPT = """
You are a friendly and knowledgeable AI assistant.
Keep your answers concise but complete.
If you don't know something, say so honestly.
"""

def chat(messages: list) -> str:
    """Send the current message history and return the assistant reply."""
    response = ollama.chat(
        model="llama3.2",
        messages=messages,
        stream=False
    )
    return response["message"]["content"]


def main():
    print("AI Chatbot (type 'quit' or 'exit' to stop, 'clear' to reset)")
    print("-" * 60)

    # The conversation history — starts with the system prompt
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            history = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Conversation cleared.")
            continue

        # Add the user message to history
        history.append({"role": "user", "content": user_input})

        # Get the assistant's reply
        reply = chat(history)

        # Add the assistant reply to history so the next call includes it
        history.append({"role": "assistant", "content": reply})

        print(f"\nAssistant: {reply}")


if __name__ == "__main__":
    main()
```

Run it with `python chatbot.py` and have a full conversation. Notice you can refer back to earlier messages — "what was my first question?" — and the model will know because it has the full history.

### Adding Streaming to the Chatbot (20:00 – 24:00)

**Host (voiceover):**
Let's make it feel more alive with streaming. Replace the `chat()` function and the print statement:

```python
def chat_streaming(messages: list) -> str:
    """Stream the reply to the terminal; return the full text."""
    stream = ollama.chat(
        model="llama3.2",
        messages=messages,
        stream=True
    )

    print("\nAssistant: ", end="", flush=True)
    full_reply = ""
    for chunk in stream:
        token = chunk["message"]["content"]
        print(token, end="", flush=True)
        full_reply += token
    print()  # newline after stream ends

    return full_reply
```

And in `main()`, call `chat_streaming(history)` instead of `chat(history)`.

---

## Episode 3 — Managing Context Length (24:00 – 27:00)

### The Context Window Problem (24:00 – 25:30)

**Host (voiceover):**
LLMs can only process a limited amount of text at once — the **context window**. For Llama 3.2, that's 128,000 tokens — quite large. But in a very long conversation, you could hit that limit, and older messages get cut off.

A simple fix: **trim the oldest non-system messages** when the history gets too long.

### Implementing a Simple Trim (25:30 – 27:00)

```python
MAX_HISTORY_MESSAGES = 20  # keep system + last 20 turns

def trim_history(history: list) -> list:
    """Keep the system prompt and the most recent messages."""
    system_messages = [m for m in history if m["role"] == "system"]
    other_messages  = [m for m in history if m["role"] != "system"]

    if len(other_messages) > MAX_HISTORY_MESSAGES:
        other_messages = other_messages[-MAX_HISTORY_MESSAGES:]

    return system_messages + other_messages
```

Call `history = trim_history(history)` before each `ollama.chat()` call.

---

## Season Wrap-Up (27:00 – 30:00)

*[Host on camera]*

**Host:**
Massive progress this season! You learned:

- ✅ The role of system, user, and assistant messages
- ✅ Five core prompt engineering techniques
- ✅ How to maintain conversation history for multi-turn chat
- ✅ Streaming responses
- ✅ Trimming history to avoid context limit issues

In **Season 4** we tackle three advanced projects: **RAG** (giving your LLM access to your own documents), **function calling**, and a polished CLI app using the `rich` library.

See you there!

*[Outro music]*

---

## 🏋️ Practice Project

Enhance the chatbot with:
1. A `/save` command that writes the conversation to `chat_history.txt`
2. A `/load` command that reads a previously saved conversation
3. Display a `[tokens: ~N]` estimate after each assistant reply (count words × 1.3 as a rough token estimate)

Sample solution: `code/practice_solution.py`
