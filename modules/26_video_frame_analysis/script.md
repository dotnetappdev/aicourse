# Module 26 — Video Analysis: Extract & Analyse Key Frames
**~8 min · Video AI**

---

## Script

**Host:**
A video is just a sequence of images. With OpenCV we can extract frames, and with LLaVA we can understand what's happening in each one. In this module we'll build a pipeline that watches a video, picks the most interesting moments, and generates a written summary — entirely locally.

### Installing OpenCV

```bash
pip install opencv-python
```

### Extracting Frames with OpenCV

```python
import cv2, pathlib, math

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

    fps        = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_step = max(1, math.floor(fps * every_n_seconds))
    out_dir    = pathlib.Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    saved  = []
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_step == 0:
            timestamp  = frame_idx / fps
            filename   = out_dir / f"frame_{frame_idx:06d}_{timestamp:.1f}s.jpg"
            cv2.imwrite(str(filename), frame)
            saved.append(str(filename))
        frame_idx += 1

    cap.release()
    return saved
```

### Detecting Scene Changes

Not all frames are equally interesting. We can skip near-duplicate frames by measuring how much the image changes:

```python
import numpy as np

def frames_with_scene_changes(
    video_path: str,
    output_dir: str,
    threshold: float = 30.0,
    min_gap_seconds: float = 1.0,
) -> list[str]:
    """
    Save only frames where a significant scene change is detected.

    `threshold` is the mean absolute pixel difference between consecutive frames.
    Higher values = only catch big changes; lower values = more frames.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    fps      = cap.get(cv2.CAP_PROP_FPS) or 25
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
            diff = np.mean(np.abs(gray.astype(float) - prev_gray.astype(float)))
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
```

### Analysing Each Frame with LLaVA

```python
import ollama

def describe_frame(image_path: str, context: str = "", model: str = "llava") -> str:
    """Generate a one-sentence description of a video frame."""
    context_line = f"Context: {context}\n" if context else ""
    prompt = (
        f"{context_line}"
        "Describe what is happening in this video frame in one clear sentence. "
        "Focus on the main action or subject."
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    return response["message"]["content"].strip()
```

### Generating a Video Summary

```python
def summarise_video(
    video_path: str,
    model: str = "llava",
    every_n_seconds: float = 3.0,
    use_scene_detection: bool = True,
) -> dict:
    """
    Full pipeline: extract frames → describe each → write a summary.

    Returns:
        {
            "frames":      [{"file": ..., "timestamp": ..., "description": ...}],
            "summary":     "overall narrative paragraph",
        }
    """
    import tempfile, os

    tmp_dir = tempfile.mkdtemp(prefix="video_frames_")
    try:
        if use_scene_detection:
            frame_paths = frames_with_scene_changes(video_path, tmp_dir)
        else:
            frame_paths = extract_frames(video_path, tmp_dir, every_n_seconds)

        print(f"  Extracted {len(frame_paths)} frames to analyse.")

        frame_results = []
        for path in frame_paths:
            name  = pathlib.Path(path).stem
            # parse timestamp from filename  e.g. frame_000150_6.0s
            parts = name.split("_")
            ts    = parts[-1].replace("s", "") if parts else "?"
            desc  = describe_frame(path, model=model)
            frame_results.append({"file": name, "timestamp": ts, "description": desc})
            print(f"  [{ts}s] {desc[:80]}")

        # Ask the LLM to write an overall summary from all descriptions
        descriptions = "\n".join(
            f"[{r['timestamp']}s] {r['description']}" for r in frame_results
        )
        summary_prompt = (
            "You are a video editor writing a summary for a client. "
            "Based on these frame-by-frame descriptions of a video, write a "
            "2–3 sentence summary of the overall content and narrative:\n\n"
            + descriptions
        )
        summary_resp = ollama.chat(
            model="llama3",   # text-only model for the summary step
            messages=[{"role": "user", "content": summary_prompt}],
        )
        return {
            "frames":  frame_results,
            "summary": summary_resp["message"]["content"].strip(),
        }
    finally:
        # Clean up temp frames
        for f in pathlib.Path(tmp_dir).iterdir():
            f.unlink()
        os.rmdir(tmp_dir)
```

### Rich Output

```python
from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table

def display_summary(result: dict) -> None:
    console = Console()

    table = Table(title="Frame Analysis", show_header=True, header_style="bold cyan")
    table.add_column("Time",        style="yellow",  no_wrap=True)
    table.add_column("Description", style="white",   ratio=5)

    for frame in result["frames"]:
        table.add_row(f"{frame['timestamp']}s", frame["description"])

    console.print(table)
    console.print(Panel(
        result["summary"],
        title="[bold green]Video Summary[/bold green]",
        border_style="green",
    ))
```

---

## Practice

Take a short video clip (10–30 seconds) from your phone and run it through the pipeline. Try adjusting `every_n_seconds` and `threshold` to see how they change what gets captured.

**Tip:** `use_scene_detection=True` works best for videos with clear cuts (e.g. presentations); `every_n_seconds` mode works better for continuous footage.
