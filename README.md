# AI Development Course: From Zero to Local LLM

A beginner-friendly video course that teaches the fundamentals of AI development using Python and locally-run large language models (LLMs). No cloud API keys required — everything runs on your own machine.

---

## 🎯 Who Is This For?

- Complete beginners with little or no programming experience
- Developers curious about AI who want to avoid cloud costs
- Anyone who wants to run LLMs privately, on their own hardware

---

## 📺 27-Module Course Structure

Each module is a **focused, ~5–8 minute lesson** with its own video script and small, single-topic code file(s).

### 🐍 Python Fundamentals (Modules 1–10)

| # | Module | Key Skills | Files |
|---|--------|-----------|-------|
| 01 | [Hello World & Print](modules/01_hello_world/) | `print()`, running Python | `hello.py` |
| 02 | [Variables & Data Types](modules/02_variables/) | str, int, float, bool | `variables.py` |
| 03 | [Strings & F-Strings](modules/03_strings/) | string methods, f-strings | `strings.py` |
| 04 | [Numbers & Operators](modules/04_numbers/) | arithmetic, math module | `numbers.py` |
| 05 | [Conditionals](modules/05_conditionals/) | if / elif / else | `conditionals.py` |
| 06 | [For Loops](modules/06_for_loops/) | range, enumerate, comprehensions | `for_loops.py` |
| 07 | [While Loops](modules/07_while_loops/) | while, break, input validation | `while_loops.py` |
| 08 | [Functions](modules/08_functions/) | def, return, parameters, scope | `functions.py` |
| 09 | [Lists](modules/09_lists/) | indexing, slicing, list methods | `lists.py` |
| 10 | [Dictionaries & Files](modules/10_dictionaries_and_files/) | dicts, file I/O, JSON | `dictionaries_and_files.py` |

### 🤖 AI & LLM Fundamentals (Modules 11–14)

| # | Module | Key Skills | Files |
|---|--------|-----------|-------|
| 11 | [What Is AI, ML & LLMs?](modules/11_what_is_ai/) | concepts, terminology, quiz | `ai_concepts.py` |
| 12 | [Installing Ollama](modules/12_installing_ollama/) | setup, model download, CLI | `ollama_setup.py` |
| 13 | [First Python Chat](modules/13_first_python_chat/) | `ollama.chat()`, message format | `first_chat.py`, `qa_bot.py` |
| 14 | [Streaming Responses](modules/14_streaming/) | `stream=True`, token-by-token | `streaming.py` |

### 🎨 Prompt Engineering (Modules 15–18)

| # | Module | Key Skills | Files |
|---|--------|-----------|-------|
| 15 | [System Prompts](modules/15_system_prompts/) | personas, roles, constraints | `system_prompts.py` |
| 16 | [Prompt Techniques](modules/16_prompt_engineering/) | few-shot, CoT, formatting | `prompt_techniques.py` |
| 17 | [Multi-Turn Chatbot](modules/17_chatbot/) | conversation history, /commands | `chatbot.py` |
| 18 | [Context Management](modules/18_context_management/) | trimming, token estimation | `context_management.py` |

### 🚀 Advanced Projects (Modules 19–20)

| # | Module | Key Skills | Files |
|---|--------|-----------|-------|
| 19 | [RAG with ChromaDB](modules/19_rag/) | embeddings, vector search, grounded answers | `rag_pipeline.py` |
| 20 | [Structured Output & Rich CLI](modules/20_structured_output_and_rich/) | JSON mode, rich terminal UI | `structured_output.py`, `rich_chat.py` |

### 👁️ Vision AI (Modules 21–27)

| # | Module | Key Skills | Files |
|---|--------|-----------|-------|
| 21 | [Image Classification](modules/21_vision_image_classification/) | LLaVA, multimodal, hot dog / not hot dog | `image_classifier.py` |
| 22 | [Receipt Scanner](modules/22_vision_receipt_scanner/) | OCR, structured JSON extraction, Rich display | `receipt_scanner.py` |
| 23 | [Licence Plate ANPR & Tax Check](modules/23_vision_anpr_tax_check/) | plate OCR, normalisation, DVLA API | `anpr.py` |
| 24 | [Face Emotion Detection](modules/24_vision_emotion_detection/) | facial expression analysis, group mood, timeline | `emotion_detector.py` |
| 25 | [Object Detection & Counting](modules/25_vision_object_counting/) | count objects, multi-type inventory, crowd estimation | `object_counter.py` |
| 26 | [Video Frame Analysis](modules/26_video_frame_analysis/) | OpenCV, scene-change detection, video summary | `video_analyser.py` |
| 27 | [Live Webcam Captioning](modules/27_webcam_live_caption/) | real-time capture, smart change detection, overlay | `webcam_caption.py` |

---

## 🛠️ Prerequisites

- A computer running Windows, macOS, or Linux
- Python 3.10+ ([download](https://www.python.org/downloads/))
- [Ollama](https://ollama.com) (installed in Module 12)
- At least 4 GB RAM (8 GB recommended; Vision modules need 8 GB+)
- Vision modules (21–27): `ollama pull llava` (~4 GB) or `ollama pull llava-phi3` (~2 GB)
- Video modules (26–27): `pip install opencv-python`

---

## 🚀 Quick Start

```bash
# Clone this repository
git clone https://github.com/dotnetappdev/aicourse.git
cd aicourse

# Install Python dependencies
pip install -r requirements.txt

# Start from Module 01
cd modules/01_hello_world
python hello.py
```

---

## 📁 Repository Layout

```
aicourse/
├── README.md
├── requirements.txt
└── modules/
    ├── 01_hello_world/
    │   ├── script.md     ← video script (~5-8 min)
    │   └── hello.py      ← focused code file
    ├── 02_variables/
    │   ├── script.md
    │   └── variables.py
    │   ...
    └── 20_structured_output_and_rich/
        ├── script.md
        ├── structured_output.py
        └── rich_chat.py
```

---

## 📝 License

MIT — free to use, share, and adapt for your own teaching.
