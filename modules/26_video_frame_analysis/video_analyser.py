# video_analyser.py — Module 26
"""
Extract key frames from a video and analyse them with a local LLaVA model.

Requirements:
    pip install ollama opencv-python rich
    ollama pull llava
    ollama pull llama3    # used for the final text-only summary step

Usage:
    python video_analyser.py clip.mp4
    python video_analyser.py clip.mp4 --every 5 --no-scene-detect
    python video_analyser.py clip.mp4 --output-dir frames/
"""

import argparse
import math
import os
import pathlib
import sys
import tempfile

import cv2
import numpy as np
import ollama
from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table

MODEL_VISION = "llava"
MODEL_TEXT   = "llama3"   # text-only model for the summary step
console      = Console()


# ── Frame extraction ──────────────────────────────────────────────────────

def extract_frames(
    video_path: str,
    output_dir: str,
    every_n_seconds: float = 2.0,
) -> list[str]:
    """
    Extract one frame every `every_n_seconds` from a video.
    Returns a list of saved frame file paths.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    fps        = cap.get(cv2.CAP_PROP_FPS) or 25.0
    frame_step = max(1, math.floor(fps * every_n_seconds))
    out_dir    = pathlib.Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    saved     = []
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_step == 0:
            timestamp = frame_idx / fps
            filename  = out_dir / f"frame_{frame_idx:06d}_{timestamp:.1f}s.jpg"
            cv2.imwrite(str(filename), frame)
            saved.append(str(filename))
        frame_idx += 1

    cap.release()
    return saved


def extract_scene_change_frames(
    video_path: str,
    output_dir: str,
    threshold: float = 30.0,
    min_gap_seconds: float = 1.0,
) -> list[str]:
    """
    Save only frames where a significant scene change is detected.

    `threshold`: mean absolute pixel difference between consecutive frames.
    Higher = only big changes captured; lower = more frames.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    fps      = cap.get(cv2.CAP_PROP_FPS) or 25.0
    min_gap  = int(fps * min_gap_seconds)
    out_dir  = pathlib.Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    saved      = []
    prev_gray  = None
    frame_idx  = 0
    last_saved = -min_gap

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_gray is not None:
            diff = float(np.mean(np.abs(gray.astype(float) - prev_gray.astype(float))))
            if diff > threshold and (frame_idx - last_saved) >= min_gap:
                timestamp = frame_idx / fps
                filename  = out_dir / f"scene_{frame_idx:06d}_{timestamp:.1f}s.jpg"
                cv2.imwrite(str(filename), frame)
                saved.append(str(filename))
                last_saved = frame_idx

        prev_gray = gray
        frame_idx += 1

    cap.release()
    return saved


# ── Analysis ──────────────────────────────────────────────────────────────

def describe_frame(image_path: str) -> str:
    """Generate a one-sentence description of a video frame using LLaVA."""
    prompt = (
        "Describe what is happening in this video frame in one clear sentence. "
        "Focus on the main action or subject."
    )
    response = ollama.chat(
        model=MODEL_VISION,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return response["message"]["content"].strip()


def generate_summary(frame_descriptions: list[dict]) -> str:
    """Use a text LLM to write an overall video summary from frame descriptions."""
    descriptions = "\n".join(
        f"[{r['timestamp']}s] {r['description']}" for r in frame_descriptions
    )
    prompt = (
        "You are a video editor writing a summary for a client. "
        "Based on these frame-by-frame descriptions, write a 2–3 sentence summary "
        "of the overall content and narrative:\n\n" + descriptions
    )
    response = ollama.chat(
        model=MODEL_TEXT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"].strip()


def analyse_video(
    video_path: str,
    every_n_seconds: float = 3.0,
    scene_detect: bool = True,
    output_dir: str | None = None,
) -> dict:
    """
    Full pipeline: extract frames → describe each → write a summary.

    Returns:
        {frames: [{file, timestamp, description}], summary: str}
    """
    tmp_dir    = output_dir or tempfile.mkdtemp(prefix="video_frames_")
    keep_files = output_dir is not None

    try:
        if scene_detect:
            console.print("  Using scene-change detection...")
            frame_paths = extract_scene_change_frames(video_path, tmp_dir)
        else:
            console.print(f"  Extracting one frame every {every_n_seconds}s...")
            frame_paths = extract_frames(video_path, tmp_dir, every_n_seconds)

        console.print(f"  Extracted [bold]{len(frame_paths)}[/bold] frames to analyse.\n")

        frame_results = []
        for path in frame_paths:
            name  = pathlib.Path(path).stem
            parts = name.split("_")
            ts    = parts[-1].replace("s", "") if len(parts) > 1 else "?"
            desc  = describe_frame(path)
            frame_results.append({"file": name, "timestamp": ts, "description": desc})
            console.print(f"  [[yellow]{ts}s[/yellow]] {desc[:90]}")

        console.print("\n  Generating overall summary...")
        summary = generate_summary(frame_results)

        return {"frames": frame_results, "summary": summary}

    finally:
        if not keep_files:
            for f in pathlib.Path(tmp_dir).glob("*"):
                f.unlink()
            os.rmdir(tmp_dir)


# ── Display ───────────────────────────────────────────────────────────────

def display_results(result: dict) -> None:
    table = Table(title="Frame-by-Frame Analysis", header_style="bold cyan",
                  show_lines=True)
    table.add_column("Time",        style="yellow", no_wrap=True)
    table.add_column("Description", style="white",  ratio=5)

    for frame in result["frames"]:
        table.add_row(f"{frame['timestamp']}s", frame["description"])

    console.print(table)
    console.print(Panel(
        result["summary"],
        title="[bold green]Video Summary[/bold green]",
        border_style="green",
    ))


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Video frame analyser using LLaVA")
    parser.add_argument("video",          help="Path to the video file")
    parser.add_argument("--every",        type=float, default=3.0,
                        help="Seconds between frames (default: 3.0, used when "
                             "--no-scene-detect is set)")
    parser.add_argument("--no-scene-detect", action="store_true",
                        help="Extract at fixed intervals instead of scene changes")
    parser.add_argument("--output-dir",   default=None,
                        help="Save extracted frames to this directory (kept after run)")
    args = parser.parse_args()

    if not pathlib.Path(args.video).exists():
        print(f"Error: file not found: {args.video}")
        sys.exit(1)

    console.print(f"[bold]Analysing:[/bold] {args.video}\n")
    result = analyse_video(
        args.video,
        every_n_seconds=args.every,
        scene_detect=not args.no_scene_detect,
        output_dir=args.output_dir,
    )
    display_results(result)


if __name__ == "__main__":
    main()
