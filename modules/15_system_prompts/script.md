# Module 15 — System Prompts
**~6 min · Prompt Engineering**

---

## Script

**Host:**
The **system prompt** is the most powerful tool you have when working with LLMs. It tells the model who it is, how it should behave, and what it should focus on — before the user says a word.

### Adding a System Message

```python
import ollama

messages = [
    {
        "role": "system",
        "content": "You are a concise Python tutor. Always explain in plain English. Use short code examples."
    },
    {
        "role": "user",
        "content": "What is a list?"
    }
]

response = ollama.chat(model="llama3.2", messages=messages)
print(response["message"]["content"])
```

Compare this to asking the same question without a system prompt — the tutor persona makes answers much more appropriate for beginners.

### What to Put in a System Prompt

#### 1. Role / Persona
```
You are an expert senior Python developer with 10 years of experience.
```

#### 2. Tone & Style
```
Always respond in a friendly, encouraging tone.
Keep answers under 150 words unless asked for detail.
```

#### 3. Output Format
```
Format all code with triple backticks and the language name.
Always finish with a "Key Takeaway:" line.
```

#### 4. Constraints
```
Only answer questions about Python and AI.
If asked about anything else, politely redirect the conversation.
Do not make up information. If you don't know, say so.
```

#### 5. Context / Background
```
The user is a complete beginner who has just learned about variables and loops.
Assume no prior programming knowledge beyond that.
```

### Real-World Example: Customer Support Bot

```python
SYSTEM = """
You are a helpful customer support agent for TechShop, an online electronics store.

Rules:
- Only answer questions about orders, products, and shipping.
- If a customer is upset, acknowledge their frustration first.
- Always ask for an order number before checking order status.
- Do not promise refunds; say you will escalate to the billing team.
- Respond in a professional, empathetic tone.
"""
```

### System Prompt Is Persistent

The system message stays active for the entire conversation — you only need to add it once at the start of the `messages` list.

---

## Practice

Create three different personas in `personas.py`:
1. A pirate who explains programming concepts
2. A strict professor who only accepts perfect Python syntax
3. A 5-year-old explaining AI (ELI5 style)

Test each with the same question: "What is a variable?"
