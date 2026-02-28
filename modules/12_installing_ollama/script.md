# Module 12 — Installing Ollama & Downloading Models
**~6 min · AI Fundamentals**

---

## Script

**Host:**
Let's get the actual tools installed. We'll use **Ollama** — a free, open-source tool that makes running LLMs locally as simple as `git clone`.

### Install Ollama

Head to **ollama.com** and click Download.

- **macOS**: run the `.dmg`, drag to Applications, launch it — a llama appears in the menu bar.
- **Windows**: run the `.exe` installer — Ollama starts as a background service automatically.
- **Linux**:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

Verify the install:

```bash
ollama --version
```

You should see something like `ollama version 0.3.6`.

### Download Your First Model

```bash
ollama pull llama3.2
```

This downloads ~2 GB. It only happens once — models are cached locally.

Try chatting directly in the terminal:

```bash
ollama run llama3.2
```

Type `Hello!` and press Enter. Type `/bye` to exit.

### Useful Ollama Commands

```bash
ollama list                 # models you have downloaded
ollama pull mistral         # download another model
ollama rm phi3              # delete a model (frees disk space)
ollama show llama3.2        # model details (context length, etc.)
ollama ps                   # running models (if any are loaded)
```

### Recommended Starter Models

| Model | Download Size | RAM Needed | Good For |
|-------|:---:|:---:|---------|
| `llama3.2` | ~2 GB | 4 GB | General chat, fast |
| `mistral` | ~4 GB | 8 GB | Instruction following |
| `phi3` | ~2 GB | 4 GB | Coding, speed |
| `gemma2` | ~5 GB | 8 GB | Google's open model |
| `codellama` | ~4 GB | 8 GB | Code generation |
| `nomic-embed-text` | ~274 MB | 1 GB | Embeddings for RAG |

### How Ollama Works

Ollama runs a small server at `http://localhost:11434`. When you run a model, it loads into RAM. All communication between your Python code and the model goes through this local server — nothing leaves your machine.

---

## Practice

In a terminal, pull `llama3.2`, run it, and ask it: "Explain what a token is in one sentence." Write down what it says.
