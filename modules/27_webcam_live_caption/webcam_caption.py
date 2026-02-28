# webcam_caption.py — Module 27
"""
Live webcam captioning using a local LLaVA multimodal model.
Captures frames from your webcam and generates real-time descriptions.

Requirements:
    pip install ollama opencv-python rich
    ollama pull llava

Usage:
    python webcam_caption.py                    # smart mode (only when scene changes)
    python webcam_caption.py --interval 5       # caption every 5 seconds
    python webcam_caption.py --display          # show live OpenCV window with caption overlay
    python webcam_caption.py --camera 1         # use external/second camera
"""

import argparse
import os
import pathlib
import sys
import tempfile
import time

import cv2
import numpy as np
import ollama

MODEL = "llava"


# ── Frame helpers ─────────────────────────────────────────────────────────

def _save_frame(cap: cv2.VideoCapture, path: str) -> bool:
    """Capture one frame from the webcam and save it to `path`."""
    ret, frame = cap.read()
    if not ret:
        return False
    cv2.imwrite(path, frame)
    return True


def _pixel_diff(path_a: str, path_b: str) -> float:
    """Mean absolute pixel difference between two saved grayscale images."""
    a = cv2.imread(path_a, cv2.IMREAD_GRAYSCALE)
    b = cv2.imread(path_b, cv2.IMREAD_GRAYSCALE)
    if a is None or b is None or a.shape != b.shape:
        return 255.0
    return float(np.mean(np.abs(a.astype(float) - b.astype(float))))


# ── LLaVA captioning ──────────────────────────────────────────────────────

def describe_frame(image_path: str, previous: str = "") -> str:
    """Ask LLaVA to describe a webcam frame in one sentence."""
    context = (
        f"The previous description was: '{previous}'. Has anything changed? "
        if previous else ""
    )
    prompt = (
        f"{context}"
        "Describe what you see in this webcam image in one short sentence. "
        "Be direct and specific."
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return response["message"]["content"].strip()


# ── Caption modes ─────────────────────────────────────────────────────────

def live_caption(
    interval_seconds: float = 3.0,
    camera_index: int = 0,
) -> None:
    """Caption every `interval_seconds`, regardless of motion."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: could not open webcam. Try --camera 1 for a second camera.")
        sys.exit(1)

    time.sleep(0.5)   # warm up the camera
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as _f:
        tmp = _f.name
    prev   = ""
    n      = 0

    print(f"Live captioning (every {interval_seconds}s). Press Ctrl+C to stop.\n")
    try:
        while True:
            if _save_frame(cap, tmp):
                caption = describe_frame(tmp, prev)
                prev    = caption
                n      += 1
                print(f"[{n:04d}] {caption}")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        cap.release()
        if pathlib.Path(tmp).exists():
            os.unlink(tmp)


def live_caption_smart(
    interval_seconds: float = 1.0,
    change_threshold: float = 15.0,
    camera_index: int = 0,
) -> None:
    """
    Only re-caption when the scene changes significantly.

    `change_threshold`: mean pixel diff that triggers a new caption.
    Higher = fewer captions; lower = more frequent updates.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: could not open webcam.")
        sys.exit(1)

    time.sleep(0.5)
    with tempfile.NamedTemporaryFile(suffix="_prev.jpg", delete=False) as _f:
        prev_path = _f.name
    with tempfile.NamedTemporaryFile(suffix="_curr.jpg", delete=False) as _f:
        curr_path = _f.name
    prev_caption = ""
    n = 0

    print(f"Smart captioning (threshold={change_threshold}). Ctrl+C to stop.\n")
    try:
        while True:
            if not _save_frame(cap, curr_path):
                time.sleep(1)
                continue

            diff = _pixel_diff(prev_path, curr_path) if n > 0 else 255.0

            if diff >= change_threshold:
                caption      = describe_frame(curr_path, prev_caption)
                prev_caption = caption
                n           += 1
                print(f"[{n:04d}] (Δ={diff:.1f}) {caption}")
                if pathlib.Path(prev_path).exists():
                    os.unlink(prev_path)
                os.rename(curr_path, prev_path)
            else:
                print(f"       (no change, Δ={diff:.1f})")

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        cap.release()
        for p in [prev_path, curr_path]:
            if pathlib.Path(p).exists():
                os.unlink(p)


def live_caption_with_display(
    interval_seconds: float = 3.0,
    camera_index: int = 0,
) -> None:
    """
    Show a live webcam window with the AI caption overlaid.
    Press 'q' in the OpenCV window to quit.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: could not open webcam.")
        sys.exit(1)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as _f:
        tmp = _f.name
    caption   = "Waiting for first caption..."
    last_time = 0.0

    print("Webcam window open. Press 'q' to quit.\n")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            now = time.time()
            if now - last_time >= interval_seconds:
                cv2.imwrite(tmp, frame)
                caption   = describe_frame(tmp)
                last_time = now
                print(caption)

            # Overlay caption text at the bottom of the frame
            cv2.putText(
                frame,
                caption[:90],
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow("Live Webcam Caption  (q to quit)", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if pathlib.Path(tmp).exists():
            os.unlink(tmp)


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Live webcam captioning with LLaVA")
    parser.add_argument("--interval",  type=float, default=3.0,
                        help="Seconds between captions (default: 3)")
    parser.add_argument("--threshold", type=float, default=15.0,
                        help="Pixel-diff threshold for smart mode (default: 15)")
    parser.add_argument("--camera",    type=int,   default=0,
                        help="Camera device index (default: 0 = built-in webcam)")
    parser.add_argument("--display",   action="store_true",
                        help="Show live OpenCV window with caption overlay")
    parser.add_argument("--simple",    action="store_true",
                        help="Caption every interval (no change detection)")
    args = parser.parse_args()

    if args.display:
        live_caption_with_display(args.interval, args.camera)
    elif args.simple:
        live_caption(args.interval, args.camera)
    else:
        live_caption_smart(args.interval, args.threshold, args.camera)


if __name__ == "__main__":
    main()
