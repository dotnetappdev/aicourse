# Module 25 — Vision AI: Object Detection & Counting
**~7 min · Vision AI**

---

## Script

**Host:**
Counting things in a photo sounds simple — until you have a car park with 200 vehicles, or a supermarket shelf with 50 products. Traditional computer vision requires training data; a multimodal LLM can do it with a plain-English prompt.

### Simple Object Count

```python
import ollama

def count_objects(image_path: str, object_name: str, model: str = "llava") -> dict:
    """Count how many instances of a specific object appear in an image."""
    prompt = (
        f"Look carefully at this image. "
        f"Count every {object_name} you can see, including partial ones at the edges. "
        f"Return your answer in this exact format:\n"
        f"Count: <number>\n"
        f"Confidence: <high / medium / low>\n"
        f"Notes: <any caveats, e.g. 'some are partially obscured'>"
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return _parse_count_response(response["message"]["content"], object_name)
```

### Parsing

```python
import re

def _parse_count_response(text: str, object_name: str) -> dict:
    count_match = re.search(r"Count:\s*(\d+)", text, re.IGNORECASE)
    conf_match  = re.search(r"Confidence:\s*(\w+)", text, re.IGNORECASE)
    notes_match = re.search(r"Notes:\s*(.+)",  text, re.IGNORECASE)
    return {
        "object":     object_name,
        "count":      int(count_match.group(1)) if count_match else -1,
        "confidence": conf_match.group(1).lower()  if conf_match  else "unknown",
        "notes":      notes_match.group(1).strip() if notes_match else "",
        "raw":        text,
    }
```

### Multi-Object Inventory

Count several different types of object in one pass:

```python
def inventory(image_path: str, objects: list[str], model: str = "llava") -> list[dict]:
    """
    Count multiple object types in a single image.

    Args:
        image_path: path to the image
        objects:    list of object names, e.g. ["car", "person", "bicycle"]

    Returns:
        List of dicts with count & confidence for each object type.
    """
    items_str = "\n".join(f"- {obj}" for obj in objects)
    prompt = (
        f"Look at this image carefully.\n"
        f"For each of the following, count how many you can see:\n{items_str}\n\n"
        f"Return ONLY a numbered list in this exact format:\n"
        + "\n".join(f"{i+1}. {obj}: <count> (<high/medium/low> confidence)"
                    for i, obj in enumerate(objects))
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return _parse_inventory(response["message"]["content"], objects)


def _parse_inventory(text: str, objects: list[str]) -> list[dict]:
    results = []
    for obj in objects:
        pattern = rf"{re.escape(obj)}:\s*(\d+)\s*\((\w+)"
        match   = re.search(pattern, text, re.IGNORECASE)
        if match:
            results.append({
                "object":     obj,
                "count":      int(match.group(1)),
                "confidence": match.group(2).lower(),
            })
        else:
            results.append({"object": obj, "count": -1, "confidence": "unknown"})
    return results
```

### Shelf & Crowd Analysis

```python
def analyse_shelf(image_path: str, product: str, model: str = "llava") -> dict:
    """Analyse a retail shelf for product stock levels."""
    prompt = (
        f"You are a retail stock checker. "
        f"Look at this shelf image and count the number of '{product}' items visible. "
        f"Also note any gaps (empty shelf spaces) that suggest out-of-stock positions.\n\n"
        f"Format:\n"
        f"Count: <number>\n"
        f"Empty gaps: <number>\n"
        f"Stock status: <well stocked / low / out of stock>\n"
        f"Notes: <any observations>"
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return {"raw": response["message"]["content"]}


def estimate_crowd_size(image_path: str, model: str = "llava") -> dict:
    """Estimate the number of people in a crowd photo."""
    prompt = (
        "Estimate the number of people visible in this image. "
        "If the crowd is dense, give a range (e.g. '50–80 people'). "
        "Format:\n"
        "Estimate: <number or range>\n"
        "Density: <sparse / moderate / dense / very dense>\n"
        "Notes: <any relevant observations>"
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return {"raw": response["message"]["content"]}
```

### Rich Terminal Output

```python
from rich.console import Console
from rich.table   import Table

def display_inventory(results: list[dict]) -> None:
    console = Console()
    table   = Table(title="Object Inventory", show_header=True,
                    header_style="bold cyan")
    table.add_column("Object",     style="white")
    table.add_column("Count",      justify="right", style="bold green")
    table.add_column("Confidence", justify="center")

    conf_colours = {"high": "green", "medium": "yellow", "low": "red"}
    for row in results:
        conf   = row["confidence"]
        colour = conf_colours.get(conf, "white")
        table.add_row(
            row["object"],
            str(row["count"]) if row["count"] >= 0 else "?",
            f"[{colour}]{conf}[/{colour}]",
        )

    console.print(table)
```

---

## Practice

Find a photo with many similar objects (a car park, a bookshelf, a fruit bowl, a crowd).
Run `object_counter.py your_photo.jpg --object "car"` and compare the AI's count with your own.
