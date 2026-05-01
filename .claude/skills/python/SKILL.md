---
name: python
description: Use when writing Python code — type hints, dataclasses, error handling, async/await, file I/O, and audio processing with librosa for backend services
---

# Python

## Overview

Write idiomatic Python: type hints everywhere, dataclasses for models, explicit error handling, and `async/await` for I/O-bound work.

## Core Patterns

### Type Hints

```python
from typing import Optional

def analyze_audio(file_path: str, duration_sec: int) -> dict:
    ...

def get_chords(key: str) -> list[str]:
    ...

def upload_file(path: str) -> Optional[str]:
    ...
```

### Dataclasses for Models

```python
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    key: str          # e.g. "G Major"
    bpm: int
    chords: list[str]

@dataclass
class AudioUpload:
    file_path: str
    duration_sec: int
```

### Error Handling

```python
# Use specific exceptions, not bare except
try:
    result = analyze_audio(path)
except FileNotFoundError:
    return {"error": "Audio file not found"}
except ValueError as e:
    return {"error": f"Invalid input: {e}"}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"error": "Analysis failed"}
```

### Async / Await (for I/O-bound work)

```python
import asyncio
import aiofiles

async def read_audio_file(path: str) -> bytes:
    async with aiofiles.open(path, "rb") as f:
        return await f.read()

async def process_upload(file_path: str) -> AnalysisResult:
    audio_bytes = await read_audio_file(file_path)
    return await run_analysis(audio_bytes)
```

### File I/O

```python
import tempfile
import os

# Safe temp file handling
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
    tmp.write(audio_bytes)
    tmp_path = tmp.name

try:
    result = analyze(tmp_path)
finally:
    os.unlink(tmp_path)  # always clean up
```

## Audio Processing (librosa)

```python
import librosa
import numpy as np

def detect_key_and_bpm(file_path: str) -> tuple[str, int]:
    y, sr = librosa.load(file_path, sr=None)

    # BPM
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = int(round(tempo))

    # Key via chroma
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    key_index = int(np.argmax(chroma_mean))
    key = PITCH_CLASSES[key_index]  # map index to note name

    return key, bpm

PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F",
                 "F#", "G", "G#", "A", "A#", "B"]
```

### Chord Suggestions (rule-based, MVP)

```python
MAJOR_CHORDS: dict[str, list[str]] = {
    "C": ["C", "F", "G", "Am"],
    "G": ["G", "C", "D", "Em"],
    "D": ["D", "G", "A", "Bm"],
    "A": ["A", "D", "E", "F#m"],
    # ... extend as needed
}

def get_chord_suggestions(key: str) -> list[str]:
    return MAJOR_CHORDS.get(key, [])
```

## Quick Reference

| Pattern | Use For |
|---|---|
| `@dataclass` | Request/response models |
| `Optional[T]` | Nullable return values |
| `try/except <Specific>` | Targeted error handling |
| `async/await` | File and network I/O |
| `tempfile.NamedTemporaryFile` | Safe temp audio file handling |
| `librosa.load` | Load audio for analysis |
| `librosa.beat.beat_track` | BPM detection |
| `librosa.feature.chroma_cqt` | Key detection via chroma |

## Common Mistakes

- Bare `except:` catches everything including `KeyboardInterrupt` — always name the exception
- Not deleting temp files — use `try/finally` or `tempfile` context managers
- Calling `librosa.load` with default `sr=22050` — use `sr=None` to preserve original sample rate
- Mixing sync and async — don't call `asyncio.run()` inside an already-running event loop
- Mutable default arguments: `def f(items=[])` — use `def f(items=None)` and assign inside
