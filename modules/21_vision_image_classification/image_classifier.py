# image_classifier.py — Module 21
"""
Vision AI image classifier using a local multimodal LLM (LLaVA).

Requirements:
    pip install ollama requests
    ollama pull llava          # ~4 GB, needs ~8 GB RAM
    # OR for a lighter model:
    ollama pull llava-phi3     # ~2 GB

Usage:
    python image_classifier.py hotdog.jpg
    python image_classifier.py my_photo.jpg --categories "cat,dog,other"
"""

import argparse
import pathlib
import sys

import requests
import ollama

MODEL = "llava"


# ── Download a test image ─────────────────────────────────────────────────

def download_image(url: str, filename: str) -> str:
    """Download an image from a URL and save it locally."""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    path = pathlib.Path(filename)
    path.write_bytes(resp.content)
    print(f"Downloaded: {path}")
    return str(path)


# ── Hot Dog Classifier ────────────────────────────────────────────────────

def is_hot_dog(image_path: str) -> dict:
    """
    Classify whether an image contains a hot dog.

    Returns a dict with:
      - is_hot_dog (bool)
      - verdict    (str)
      - raw        (str — the model's full response)
    """
    prompt = (
        "Look at this image.\n"
        "1. What food (if any) is shown?\n"
        "2. Is this a hot dog? Answer with EXACTLY one of: HOT DOG or NOT HOT DOG\n\n"
        "Format:\n"
        "Food: <name>\n"
        "Result: <HOT DOG or NOT HOT DOG>"
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    text      = response["message"]["content"]
    is_hotdog = "HOT DOG" in text.upper() and "NOT HOT DOG" not in text.upper()
    return {
        "is_hot_dog": is_hotdog,
        "verdict":    "🌭 Hot Dog!" if is_hotdog else "❌ Not Hot Dog",
        "raw":        text,
    }


# ── Generic Image Classifier ──────────────────────────────────────────────

def classify(image_path: str, categories: list[str]) -> str:
    """
    Classify an image into one of the given categories.

    Args:
        image_path: local path to the image file
        categories: list of possible labels, e.g. ["cat", "dog", "other"]

    Returns:
        The matched category string, or the raw model reply if no match.
    """
    options = " / ".join(categories)
    prompt  = (
        f"Classify the image as exactly one of: {options}. "
        "Reply with just the category name, nothing else."
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    reply = response["message"]["content"].strip().lower()
    for cat in categories:
        if cat.lower() in reply:
            return cat
    return reply


# ── CLI entry point ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Vision AI image classifier")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument(
        "--categories",
        default="hot dog,pizza,burger,salad,other",
        help='Comma-separated categories (default: "hot dog,pizza,burger,salad,other")',
    )
    parser.add_argument(
        "--hotdog", action="store_true",
        help="Run the hot-dog / not-hot-dog classifier instead",
    )
    args = parser.parse_args()

    if not pathlib.Path(args.image).exists():
        print(f"Error: file not found: {args.image}")
        sys.exit(1)

    if args.hotdog:
        result = is_hot_dog(args.image)
        print(result["verdict"])
        print(f"Model response:\n{result['raw']}")
    else:
        cats   = [c.strip() for c in args.categories.split(",")]
        label  = classify(args.image, cats)
        print(f"Classification: {label}")


if __name__ == "__main__":
    main()
