# Module 21 — Vision AI: Image Classification with a Local LLM
**~7 min · Vision AI**

---

## Script

**Host:**
Local LLMs aren't just for text. **Multimodal** models can look at images and answer questions about them — no cloud, no API key. In this module we'll build a simple image classifier inspired by the classic "hot dog / not hot dog" example from Silicon Valley.

### The Model: LLaVA

We'll use **LLaVA** (Large Language and Vision Assistant), a free multimodal model that understands both text and images.

```bash
ollama pull llava
```

LLaVA is about 4 GB and requires ~8 GB RAM. A smaller alternative is `llava-phi3` (~2 GB).

### How It Works

You pass an image alongside your text prompt. The model looks at the image and the question together:

```python
import ollama

response = ollama.chat(
    model="llava",
    messages=[{
        "role": "user",
        "content": "What food is in this image? Answer in one word.",
        "images": ["hotdog.jpg"]   # file path or URL
    }]
)

print(response["message"]["content"])
```

### Building a Hot Dog Classifier

```python
import ollama

def classify_food(image_path: str) -> dict:
    """Classify whether an image contains a hot dog."""
    prompt = """Look at this image and answer two questions:
1. What food (if any) is shown?
2. Is this a hot dog? Answer with exactly: HOT DOG or NOT HOT DOG

Format your response as:
Food: <name>
Result: <HOT DOG or NOT HOT DOG>"""

    response = ollama.chat(
        model="llava",
        messages=[{
            "role": "user",
            "content": prompt,
            "images": [image_path]
        }]
    )

    text = response["message"]["content"]
    is_hotdog = "HOT DOG" in text and "NOT HOT DOG" not in text

    return {
        "raw_response": text,
        "is_hot_dog": is_hotdog,
        "verdict": "🌭 Hot Dog!" if is_hotdog else "❌ Not Hot Dog"
    }
```

### Making It Flexible — Generic Image Classifier

```python
def classify(image_path: str, categories: list[str], model: str = "llava") -> str:
    """
    Classify an image into one of the given categories.

    Args:
        image_path: path to the image file
        categories: list of possible labels, e.g. ["cat", "dog", "other"]
        model: multimodal Ollama model to use

    Returns:
        The chosen category as a string.
    """
    options = " / ".join(categories)
    prompt = (
        f"Look at the image. Classify it as exactly one of: {options}. "
        "Reply with just the category name, nothing else."
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}]
    )
    reply = response["message"]["content"].strip().lower()

    # Match reply to the closest provided category
    for cat in categories:
        if cat.lower() in reply:
            return cat
    return reply   # return as-is if no match


# Example: classify food images
food_categories = ["hot dog", "pizza", "burger", "salad", "other"]
```

### Downloading a Test Image

If you don't have an image handy, download one with `requests`:

```python
import requests, pathlib

def download_image(url: str, filename: str) -> str:
    """Download an image and return its local path."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    path = pathlib.Path(filename)
    path.write_bytes(response.content)
    return str(path)
```

### Running in Bulk

```python
images = [
    ("tests/hotdog.jpg",  food_categories),
    ("tests/pizza.jpg",   food_categories),
    ("tests/cat.jpg",     ["cat", "dog", "other"]),
]

for img_path, cats in images:
    label = classify(img_path, cats)
    print(f"{img_path:30s} → {label}")
```

---

## Practice

Download 5 food images (use `requests` or any you have locally), run them through `classify()`, and see how accurately LLaVA labels them.

**Tip:** try the prompt "Is there a hot dog in this image? Yes or No." — sometimes simpler prompts work better than elaborate ones.
