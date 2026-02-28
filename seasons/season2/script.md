# Season 2 — AI & LLM Fundamentals
### "Understanding AI and Running Your First Local Model"
**Estimated runtime: ~30 minutes**

---

## Pre-Roll (0:00 – 0:45)

*[Intro music. Course logo animation.]*

**Host (on camera):**
Welcome back! Last season we learned Python basics — variables, functions, loops, files. You crushed it.

Today we're stepping into the world of **Artificial Intelligence**. We'll cover what AI, machine learning, and large language models actually *are*, then install **Ollama** — a tool that lets you run powerful LLMs for free on your own computer — and have our very first conversation with one.

By the end of this 30-minute session you will have an AI model running locally and you'll be chatting with it from Python code.

Let's go.

---

## Episode 1 — What Is AI, ML, and LLM? (0:45 – 9:00)

### Artificial Intelligence (0:45 – 3:00)

**Host (voiceover):**
**Artificial Intelligence** — AI — is a broad term for computer systems that perform tasks that normally require human intelligence: recognising images, understanding speech, translating languages, and answering questions.

Think of AI as the umbrella. Everything else we'll talk about lives underneath it.

### Machine Learning (3:00 – 5:30)

**Host (voiceover):**
**Machine Learning** is the most important branch of AI. Instead of a programmer writing explicit rules — "if the email contains the word *free money* then it's spam" — machine learning systems **learn** those rules automatically by looking at thousands or millions of examples.

The learning happens through a process called **training**: you feed the model labelled data, it adjusts its internal parameters (called *weights*) to minimise errors, and over time it becomes better and better at the task.

Once trained, the model can make predictions on data it has never seen before.

### Large Language Models (5:30 – 9:00)

**Host (voiceover):**
A **Large Language Model**, or LLM, is a type of machine learning model trained on an enormous amount of text — think books, websites, code, scientific papers — to understand and generate human language.

Famous examples: GPT-4 (powers ChatGPT), Claude, Gemini. But there are also **open-source** LLMs you can download and run yourself: **Llama 3**, **Mistral**, **Phi-3**, **Gemma**, and many more.

LLMs work by **predicting the next token** (roughly a word or word-piece). You give the model a prompt — a block of text — and it generates a continuation one token at a time. That's it. Everything ChatGPT does is built on that simple foundation.

Key terms you'll hear constantly:

| Term | Meaning |
|------|---------|
| **Parameters / weights** | Numbers the model learned during training. "8B" = 8 billion parameters. |
| **Context window** | How much text the model can "see" at once (measured in tokens). |
| **Token** | A chunk of text, roughly 3–4 characters on average. |
| **Quantisation** | Compressing a model so it takes less RAM/disk. Q4 = 4-bit, smaller but slightly less accurate. |
| **Prompt** | The text you send to the model as input. |
| **Inference** | Running the model to generate a response. |

---

## Episode 2 — Installing Ollama (9:00 – 17:00)

### What Is Ollama? (9:00 – 10:30)

*[Screen share: ollama.com]*

**Host (voiceover):**
**Ollama** is a free, open-source tool that makes it incredibly easy to download and run LLMs locally. Think of it like Docker, but for AI models.

It handles:
- Downloading models from a registry
- Running them efficiently using your CPU and/or GPU
- Exposing a local REST API your Python code can call

It works on Mac, Windows (via WSL or native), and Linux.

### Installation (10:30 – 13:00)

**Host (voiceover):**
Head to **ollama.com** and click **Download**. Run the installer for your operating system.

On **macOS**: the installer puts Ollama in your Applications folder. Launch it and you'll see a llama icon in your menu bar.

On **Windows**: run the `.exe` installer. Ollama will start automatically as a background service.

On **Linux**: open a terminal and run:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Once installed, open a terminal and test it:

```bash
ollama --version
```

You should see something like `ollama version 0.3.6`.

### Downloading Your First Model (13:00 – 17:00)

**Host (voiceover):**
Now let's download a model. We'll start with **Llama 3.2 3B** — it's small enough to run on most computers but smart enough to be genuinely useful.

In your terminal:

```bash
ollama pull llama3.2
```

This downloads about 2 GB. Grab a coffee — it only happens once.

Once downloaded, try chatting with it directly in the terminal:

```bash
ollama run llama3.2
```

Type `Hello! What can you do?` and press Enter. You should see a response stream back.

Type `/bye` to exit the chat.

Now let's look at what other models are available:

```bash
ollama list        # models you've downloaded
```

Some popular models to try later:

| Model | Size | Good at |
|-------|------|---------|
| `llama3.2` | 2 GB | General chat, reasoning |
| `mistral` | 4 GB | Instruction following |
| `phi3` | 2 GB | Coding, fast responses |
| `gemma2` | 5 GB | Google's open model |
| `codellama` | 4 GB | Writing and explaining code |

---

## Episode 3 — Talking to the Model from Python (17:00 – 27:00)

### The Ollama REST API (17:00 – 19:30)

**Host (voiceover):**
While the terminal chat is fun, in real AI applications we call the model from **code**. Ollama exposes a local REST API at `http://localhost:11434`.

The simplest endpoint is `/api/generate`. You send it a JSON body with a model name and a prompt, and it streams back the response.

But there's an even easier way: the official **`ollama` Python package**.

Install it:

```bash
pip install ollama
```

### First Python Chat (19:30 – 24:00)

*[Screen share: VS Code with `chat.py`]*

**Host (voiceover):**
Create a file called `chat.py`:

```python
import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "What is a large language model?"}
    ]
)

print(response["message"]["content"])
```

Run it:

```bash
python chat.py
```

You should see the model's explanation appear. Notice the structure: `messages` is a **list of dictionaries**. Each dictionary has a `role` (either `"user"` or `"assistant"`) and `content` (the actual text). This is the standard **OpenAI chat format** that nearly every LLM API uses.

### Streaming Responses (24:00 – 27:00)

**Host (voiceover):**
By default, `ollama.chat()` waits until the entire response is generated before returning. For long responses that feels slow. Let's enable **streaming**:

```python
import ollama

stream = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "Explain Python in 3 sentences."}
    ],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

print()  # newline at the end
```

With streaming, each token appears as it's generated — just like ChatGPT's "typing" effect. `end=""` prevents extra newlines between chunks, and `flush=True` makes sure each character appears immediately.

---

## Season Wrap-Up (27:00 – 30:00)

*[Host on camera]*

**Host:**
Brilliant! This season you learned:

- ✅ The difference between AI, machine learning, and LLMs
- ✅ How LLMs work (next-token prediction)
- ✅ How to install Ollama and download models
- ✅ How to call a model from Python using the `ollama` package
- ✅ How to stream responses token by token

In **Season 3** we'll go deeper: prompt engineering, building a multi-turn chatbot that remembers the conversation, and managing context length.

See you there!

*[Outro music]*

---

## 🏋️ Practice Project

Create `my_model_info.py` that:
1. Uses `ollama.list()` to get all downloaded models
2. Prints a formatted table showing each model's name and size
3. Asks the user which model they want to query
4. Asks for a question and prints the streamed response

A sample solution is in `code/practice_solution.py`.
