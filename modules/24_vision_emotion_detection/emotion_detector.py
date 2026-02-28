# emotion_detector.py — Module 24
"""
Detect emotions and facial expressions from images using a local LLaVA model.

Requirements:
    pip install ollama rich
    ollama pull llava

Usage:
    python emotion_detector.py photo.jpg
    python emotion_detector.py group_photo.jpg --group
    python emotion_detector.py frames/ --timeline
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


# ── Detection ─────────────────────────────────────────────────────────────

def detect_emotion(image_path: str) -> dict:
    """
    Detect the primary emotion shown in a face image.

    Returns:
        {emotion, confidence, description}
    """
    prompt = (
        "Look at the face in this image.\n"
        "Identify the primary emotion being expressed.\n"
        "Return your answer in this exact format:\n"
        "Emotion: <one of: happy, sad, angry, surprised, neutral, disgusted, fearful, other>\n"
        "Confidence: <high / medium / low>\n"
        "Description: <one sentence describing what you see in the face>"
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return _parse(response["message"]["content"])


def _parse(text: str) -> dict:
    emotion    = re.search(r"Emotion:\s*(\w+)",      text, re.IGNORECASE)
    confidence = re.search(r"Confidence:\s*(\w+)",   text, re.IGNORECASE)
    description = re.search(r"Description:\s*(.+)",  text, re.IGNORECASE)
    return {
        "emotion":     emotion.group(1).lower()     if emotion     else "unknown",
        "confidence":  confidence.group(1).lower()  if confidence  else "unknown",
        "description": description.group(1).strip() if description else text.strip(),
    }


def analyse_group_photo(image_path: str) -> str:
    """Return a raw text analysis of the emotional tone of a group photo."""
    prompt = (
        "Look at this group photo.\n"
        "For each clearly visible face, describe their apparent emotion.\n"
        "Then give an overall mood score for the group.\n\n"
        "Format:\n"
        "Faces:\n"
        "- Person 1: <emotion>\n"
        "- Person 2: <emotion>\n"
        "(continue for each person)\n\n"
        "Overall mood: <positive / neutral / mixed / negative>\n"
        "Group energy: <one sentence>"
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return response["message"]["content"]


def sentiment_timeline(image_folder: str) -> list[dict]:
    """
    Analyse emotion across a sequence of images in a folder.
    Files are processed in sorted order (e.g. frame_001.jpg, frame_002.jpg).
    """
    folder = pathlib.Path(image_folder)
    images = sorted(folder.glob("*.jpg")) + sorted(folder.glob("*.png"))
    if not images:
        print(f"No jpg/png files found in: {folder}")
        return []

    results = []
    for img in images:
        result       = detect_emotion(str(img))
        result["file"] = img.name
        results.append(result)
    return results


# ── Display ───────────────────────────────────────────────────────────────

def display_emotion(data: dict) -> None:
    emoji      = EMOTION_EMOJI.get(data["emotion"], "🤔")
    conf       = data["confidence"]
    conf_colour = {"high": "green", "medium": "yellow", "low": "red"}.get(conf, "white")
    console.print(
        f"\n{emoji}  [bold]Emotion:[/bold]     {data['emotion'].capitalize()}\n"
        f"   [bold]Confidence:[/bold]  [{conf_colour}]{conf}[/{conf_colour}]\n"
        f"   [bold]Description:[/bold] {data['description']}\n"
    )


def display_timeline(results: list[dict]) -> None:
    table = Table(title="Emotion Timeline", header_style="bold cyan")
    table.add_column("File",        style="dim")
    table.add_column("Emotion",     style="bold")
    table.add_column("Confidence",  justify="center")
    table.add_column("Description", ratio=4)

    conf_colours = {"high": "green", "medium": "yellow", "low": "red"}
    for r in results:
        emoji  = EMOTION_EMOJI.get(r["emotion"], "🤔")
        conf   = r["confidence"]
        colour = conf_colours.get(conf, "white")
        table.add_row(
            r.get("file", ""),
            f"{emoji} {r['emotion'].capitalize()}",
            f"[{colour}]{conf}[/{colour}]",
            r["description"],
        )
    console.print(table)


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Face emotion detector using LLaVA")
    parser.add_argument("input",     help="Image file or folder of images")
    parser.add_argument("--group",    action="store_true", help="Group photo analysis")
    parser.add_argument("--timeline", action="store_true", help="Analyse a folder of images")
    args = parser.parse_args()

    path = pathlib.Path(args.input)

    if args.timeline or path.is_dir():
        results = sentiment_timeline(str(path))
        display_timeline(results)
    elif args.group:
        if not path.exists():
            print(f"Error: file not found: {path}")
            sys.exit(1)
        console.print(analyse_group_photo(str(path)))
    else:
        if not path.exists():
            print(f"Error: file not found: {path}")
            sys.exit(1)
        result = detect_emotion(str(path))
        display_emotion(result)


if __name__ == "__main__":
    main()
