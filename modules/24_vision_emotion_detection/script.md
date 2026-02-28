# Module 24 — Vision AI: Face Emotion & Sentiment Detection
**~7 min · Vision AI**

---

## Script

**Host:**
Your phone's camera app can tell when you're smiling. In this module we'll replicate that using a completely local multimodal LLM. We'll detect emotions, describe facial expressions, and build a simple sentiment meter — no cloud, no privacy concerns.

### What We're Detecting

Emotions a model can recognise from a face photo:
- **Happy** — smiling, raised cheeks
- **Sad** — downturned mouth, furrowed brow
- **Angry** — furrowed brow, set jaw
- **Surprised** — wide eyes, open mouth
- **Neutral** — relaxed face
- **Disgusted / Fearful** — rarer, but detectable in clear photos

### Basic Emotion Detection

```python
import ollama

def detect_emotion(image_path: str, model: str = "llava") -> dict:
    """Detect the primary emotion shown in a face image."""
    prompt = """Look at the face in this image.
Identify the primary emotion being expressed.
Return your answer in this exact format:
Emotion: <one of: happy, sad, angry, surprised, neutral, disgusted, fearful, other>
Confidence: <high / medium / low>
Description: <one sentence describing what you see in the face>"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return _parse_emotion_response(response["message"]["content"])
```

### Parsing the Response

```python
import re

def _parse_emotion_response(text: str) -> dict:
    emotion    = re.search(r"Emotion:\s*(\w+)",     text, re.IGNORECASE)
    confidence = re.search(r"Confidence:\s*(\w+)",  text, re.IGNORECASE)
    description = re.search(r"Description:\s*(.+)", text, re.IGNORECASE)
    return {
        "emotion":     emotion.group(1).lower()     if emotion     else "unknown",
        "confidence":  confidence.group(1).lower()  if confidence  else "unknown",
        "description": description.group(1).strip() if description else text.strip(),
    }
```

### Multi-Face Group Photo Analysis

```python
def analyse_group_photo(image_path: str, model: str = "llava") -> dict:
    """Analyse the overall emotional tone of a group photo."""
    prompt = """Look at this group photo.
For each clearly visible face, describe their apparent emotion.
Then give an overall mood score for the group.

Format:
Faces:
- Person 1: <emotion>
- Person 2: <emotion>
(continue for each person)

Overall mood: <positive / neutral / mixed / negative>
Group energy: <one sentence>"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return {"raw": response["message"]["content"]}
```

### Building a Sentiment Timeline

If you have a series of photos (e.g. frames from a meeting recording), you can track how mood changes over time:

```python
import pathlib

def sentiment_timeline(image_folder: str, model: str = "llava") -> list[dict]:
    """
    Analyse emotion across a sequence of images in a folder.
    Files are processed in alphabetical order (e.g. frame_001.jpg, frame_002.jpg).
    """
    folder  = pathlib.Path(image_folder)
    images  = sorted(folder.glob("*.jpg")) + sorted(folder.glob("*.png"))
    results = []

    for img in images:
        result = detect_emotion(str(img), model)
        result["file"] = img.name
        results.append(result)
        print(f"  {img.name:30s} → {result['emotion']:10s} ({result['confidence']})")

    return results
```

### Visualising Results in the Terminal

```python
from rich.console import Console
from rich.table   import Table

EMOTION_EMOJI = {
    "happy":     "😊",
    "sad":       "😢",
    "angry":     "😠",
    "surprised": "😲",
    "neutral":   "😐",
    "disgusted": "🤢",
    "fearful":   "😨",
    "other":     "🤔",
}

def display_emotion(data: dict) -> None:
    console = Console()
    emoji   = EMOTION_EMOJI.get(data["emotion"], "🤔")
    conf_colour = {"high": "green", "medium": "yellow", "low": "red"}.get(
        data["confidence"], "white"
    )
    console.print(
        f"\n{emoji}  Emotion:     [bold]{data['emotion'].capitalize()}[/bold]\n"
        f"   Confidence:  [{conf_colour}]{data['confidence']}[/{conf_colour}]\n"
        f"   Description: {data['description']}"
    )
```

---

## Practice

1. Take a selfie or find a portrait photo.
2. Run `emotion_detector.py your_photo.jpg` and see what the model detects.
3. Try the same face with different lighting — does it change the result?
4. Use `sentiment_timeline()` on a folder of frames from a short video clip.
