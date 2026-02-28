# Module 20 — Structured Output & Rich CLI
**~7 min · Advanced Projects**

---

## Script

**Host:**
Two final topics that make your apps feel professional: getting structured JSON from the LLM, and building beautiful terminal UIs with the `rich` library.

---

### Part A — Structured JSON Output

Sometimes you need data, not prose. Ask the model for JSON and use `format="json"` to guarantee valid JSON comes back.

```bash
pip install ollama
```

```python
import json
import ollama

def extract_info(review: str) -> dict:
    prompt = f"""Extract info from this product review.
Return ONLY valid JSON with these keys:
  product_name, rating (1-5 int), pros (list), cons (list), would_recommend (bool)

Review: "{review}"
JSON:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
        format="json",   # <-- guarantees valid JSON output
    )
    return json.loads(response["message"]["content"])
```

The `format="json"` parameter tells Ollama to enforce valid JSON — the model will not emit any text outside the JSON structure.

#### Validating the Result

Always validate LLM output before using it in your app:

```python
def is_valid(data: dict) -> bool:
    required = {"product_name", "rating", "pros", "cons", "would_recommend"}
    return (
        required.issubset(data.keys())
        and isinstance(data["rating"], int)
        and 1 <= data["rating"] <= 5
    )
```

---

### Part B — Rich Terminal UI

```bash
pip install rich
```

`rich` turns plain terminal output into polished, formatted text with colours, markdown, tables, and spinners.

```python
from rich.console  import Console
from rich.panel    import Panel
from rich.markdown import Markdown
from rich.prompt   import Prompt

console = Console()

# Panel with colour border
console.print(Panel("Hello from Rich!", title="Module 20", border_style="cyan"))

# Render markdown
console.print(Markdown("**Bold text** and `code` and a list:\n- Item 1\n- Item 2"))

# Spinner while waiting
with console.status("[bold green]Thinking...[/]", spinner="dots"):
    import time; time.sleep(2)  # simulate work
console.print("[bold green]Done![/]")

# Styled prompt
name = Prompt.ask("[bold yellow]What is your name[/]")
console.print(f"Hello, [bold cyan]{name}[/]!")
```

### Combining Both: Rich Chatbot with JSON Logging

```python
import json, ollama
from rich.console  import Console
from rich.panel    import Panel
from rich.markdown import Markdown
from rich.prompt   import Prompt

console = Console()
history = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    question = Prompt.ask("[bold yellow]You[/]").strip()
    if question.lower() == "quit":
        break

    history.append({"role": "user", "content": question})
    stream = ollama.chat(model="llama3.2", messages=history, stream=True)

    reply = ""
    with console.status("[bold green]Thinking...[/]", spinner="dots"):
        for chunk in stream:
            reply += chunk["message"]["content"]

    console.print(Panel(Markdown(reply), title="[cyan]Assistant[/]", border_style="cyan"))
    history.append({"role": "assistant", "content": reply})
```

---

## Practice

Combine everything: build a `product_reviewer.py` that takes a product name from the user, asks the LLM to generate a mock review in JSON format, validates it, and then displays it beautifully using `rich`.

Congratulations — you've completed the course! 🎉
