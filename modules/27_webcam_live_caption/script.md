# Module 27 — Vision AI: Live Webcam Captioning
**~7 min · Video AI**

---

## Script

**Host:**
What if your computer could narrate what it sees in real time? In this module we'll use OpenCV to grab frames from your webcam, send them to LLaVA, and speak the descriptions back. It's a real accessibility tool — and a fun demo to show people.

### The Core Loop

```python
import cv2, time, base64, pathlib
import ollama

def capture_frame_to_file(cap: cv2.VideoCapture, path: str) -> bool:
    """Capture a single frame and save it to disk."""
    ret, frame = cap.read()
    if not ret:
        return False
    cv2.imwrite(path, frame)
    return True


def describe_frame(image_path: str, previous: str = "", model: str = "llava") -> str:
    """Ask LLaVA to describe a webcam frame in one sentence."""
    context = (
        f"The previous description was: '{previous}'. "
        "Has anything changed? " if previous else ""
    )
    prompt = (
        f"{context}"
        "Describe what you see in this webcam image in one short sentence. "
        "Be direct and specific."
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return response["message"]["content"].strip()
```

### Live Caption Loop

```python
import tempfile, os, sys

def live_caption(
    interval_seconds: float = 3.0,
    model: str = "llava",
    camera_index: int = 0,
) -> None:
    """
    Continuously capture from the webcam and print a caption every
    `interval_seconds`.

    Press Ctrl+C to stop.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: could not open webcam. Try --camera 1 for an external camera.")
        sys.exit(1)

    # Give the camera a moment to warm up
    time.sleep(0.5)

    tmp_path   = tempfile.mktemp(suffix=".jpg")
    previous   = ""
    caption_n  = 0

    print(f"Live captioning started (every {interval_seconds}s). Press Ctrl+C to stop.\n")
    try:
        while True:
            if not capture_frame_to_file(cap, tmp_path):
                print("Warning: failed to read frame, retrying...")
                time.sleep(1)
                continue

            caption   = describe_frame(tmp_path, previous, model)
            previous  = caption
            caption_n += 1
            print(f"[{caption_n:04d}] {caption}")

            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        cap.release()
        if pathlib.Path(tmp_path).exists():
            os.unlink(tmp_path)
```

### Adding Change Detection

Sending every frame to LLaVA is wasteful if nothing changes. We can skip frames where the scene is mostly static:

```python
import numpy as np

def _mean_pixel_diff(path_a: str, path_b: str) -> float:
    """Return the mean absolute pixel difference between two images."""
    a = cv2.imread(path_a, cv2.IMREAD_GRAYSCALE)
    b = cv2.imread(path_b, cv2.IMREAD_GRAYSCALE)
    if a is None or b is None or a.shape != b.shape:
        return 255.0
    return float(np.mean(np.abs(a.astype(float) - b.astype(float))))


def live_caption_smart(
    interval_seconds: float = 1.0,
    change_threshold: float = 15.0,
    model: str = "llava",
    camera_index: int = 0,
) -> None:
    """
    Smart live captioning: only re-describe the scene when it changes
    significantly (saves time and avoids repeated identical captions).

    `change_threshold`: mean pixel diff required to trigger a new caption.
    Higher = only big changes; lower = more frequent updates.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: could not open webcam.")
        sys.exit(1)

    time.sleep(0.5)

    prev_path  = tempfile.mktemp(suffix="_prev.jpg")
    curr_path  = tempfile.mktemp(suffix="_curr.jpg")
    previous   = ""
    caption_n  = 0

    print(f"Smart live captioning (threshold={change_threshold}). Ctrl+C to stop.\n")
    try:
        while True:
            if not capture_frame_to_file(cap, curr_path):
                time.sleep(1)
                continue

            diff = _mean_pixel_diff(prev_path, curr_path) if caption_n > 0 else 255.0

            if diff >= change_threshold:
                caption   = describe_frame(curr_path, previous, model)
                previous  = caption
                caption_n += 1
                print(f"[{caption_n:04d}] (Δ={diff:.1f}) {caption}")
                # rotate files
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
```

### Showing the Webcam Feed with Captions Overlaid

```python
def live_caption_with_display(
    interval_seconds: float = 3.0,
    model: str = "llava",
    camera_index: int = 0,
) -> None:
    """
    Show a live webcam window with the current caption overlaid.
    Press 'q' to quit.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: could not open webcam.")
        sys.exit(1)

    tmp_path   = tempfile.mktemp(suffix=".jpg")
    caption    = "Waiting for first caption..."
    last_time  = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()
        if now - last_time >= interval_seconds:
            cv2.imwrite(tmp_path, frame)
            caption   = describe_frame(tmp_path, model=model)
            last_time = now

        # Draw caption on frame
        cv2.putText(
            frame, caption[:80],          # truncate long captions
            (10, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2,
            cv2.LINE_AA,
        )
        cv2.imshow("Live Webcam Caption (press q to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    if pathlib.Path(tmp_path).exists():
        os.unlink(tmp_path)
```

---

## Practice

1. Run `live_caption_smart` and wave your hand in front of the camera — watch the captions update only when you move.
2. Try `live_caption_with_display` to see the caption overlaid live.
3. Change the prompt to something domain-specific, e.g. "Describe the objects on the desk" or "Is there a person visible?".
