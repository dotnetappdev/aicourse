# object_counter.py — Module 25
"""
Count objects in images using a local LLaVA multimodal model.

Requirements:
    pip install ollama rich
    ollama pull llava

Usage:
    python object_counter.py photo.jpg --object car
    python object_counter.py shelf.jpg --object "bottle" --shelf
    python object_counter.py crowd.jpg --crowd
    python object_counter.py scene.jpg --inventory "car,person,bicycle,dog"
"""

import argparse
import pathlib
import re
import sys

import ollama
from rich.console import Console
from rich.table   import Table

MODEL   = "llava"
console = Console()


# ── Counting ──────────────────────────────────────────────────────────────

def count_objects(image_path: str, object_name: str) -> dict:
    """
    Count how many instances of a specific object appear in an image.

    Returns:
        {object, count, confidence, notes}
    """
    prompt = (
        f"Look carefully at this image. "
        f"Count every {object_name} you can see, including partial ones at the edges.\n"
        f"Return your answer in this exact format:\n"
        f"Count: <number>\n"
        f"Confidence: <high / medium / low>\n"
        f"Notes: <any caveats, e.g. 'some are partially obscured'>"
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return _parse_count(response["message"]["content"], object_name)


def _parse_count(text: str, object_name: str) -> dict:
    count_m = re.search(r"Count:\s*(\d+)",   text, re.IGNORECASE)
    conf_m  = re.search(r"Confidence:\s*(\w+)", text, re.IGNORECASE)
    notes_m = re.search(r"Notes:\s*(.+)",    text, re.IGNORECASE)
    return {
        "object":     object_name,
        "count":      int(count_m.group(1)) if count_m else -1,
        "confidence": conf_m.group(1).lower()  if conf_m  else "unknown",
        "notes":      notes_m.group(1).strip() if notes_m else "",
        "raw":        text,
    }


def inventory(image_path: str, objects: list[str]) -> list[dict]:
    """
    Count multiple object types in a single image in one model call.

    Returns a list of {object, count, confidence} dicts.
    """
    items_str = "\n".join(f"- {obj}" for obj in objects)
    format_lines = "\n".join(
        f"{i + 1}. {obj}: <count> (<high/medium/low> confidence)"
        for i, obj in enumerate(objects)
    )
    prompt = (
        f"Look at this image carefully.\n"
        f"For each of the following objects, count how many you can see:\n"
        f"{items_str}\n\n"
        f"Return ONLY a numbered list in this exact format:\n"
        f"{format_lines}"
    )
    response = ollama.chat(
        model=MODEL,
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


def analyse_shelf(image_path: str, product: str) -> dict:
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
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return {"product": product, "raw": response["message"]["content"]}


def estimate_crowd(image_path: str) -> dict:
    """Estimate the number of people in a crowd photo."""
    prompt = (
        "Estimate the number of people visible in this image. "
        "If the crowd is dense, give a range (e.g. '50–80 people').\n"
        "Format:\n"
        "Estimate: <number or range>\n"
        "Density: <sparse / moderate / dense / very dense>\n"
        "Notes: <any relevant observations>"
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return {"raw": response["message"]["content"]}


# ── Display ───────────────────────────────────────────────────────────────

def display_count(result: dict) -> None:
    conf_colour = {"high": "green", "medium": "yellow", "low": "red"}.get(
        result["confidence"], "white"
    )
    count_str = str(result["count"]) if result["count"] >= 0 else "?"
    console.print(
        f"\n[bold]{result['object'].capitalize()}s found:[/bold] "
        f"[bold green]{count_str}[/bold green]  "
        f"(confidence: [{conf_colour}]{result['confidence']}[/{conf_colour}])"
    )
    if result.get("notes"):
        console.print(f"Notes: {result['notes']}")


def display_inventory(results: list[dict]) -> None:
    table = Table(title="Object Inventory", header_style="bold cyan")
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


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Object counter using LLaVA")
    parser.add_argument("image",      help="Path to the image file")
    parser.add_argument("--object",   help="Object to count (single)")
    parser.add_argument("--inventory", help="Comma-separated list of objects to count")
    parser.add_argument("--shelf",    action="store_true", help="Retail shelf analysis")
    parser.add_argument("--crowd",    action="store_true", help="Crowd size estimation")
    args = parser.parse_args()

    if not pathlib.Path(args.image).exists():
        print(f"Error: file not found: {args.image}")
        sys.exit(1)

    if args.crowd:
        result = estimate_crowd(args.image)
        console.print(result["raw"])
    elif args.shelf and args.object:
        result = analyse_shelf(args.image, args.object)
        console.print(result["raw"])
    elif args.inventory:
        objs    = [o.strip() for o in args.inventory.split(",")]
        results = inventory(args.image, objs)
        display_inventory(results)
    elif args.object:
        result = count_objects(args.image, args.object)
        display_count(result)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
