---
name: flask
description: Use when building Flask API endpoints — routing, request parsing, file uploads, error handling, blueprints, and returning JSON responses
---

# Flask

## Overview

Lightweight Python web framework. Use blueprints for route organisation, `request` for input, `jsonify` for output, and proper HTTP status codes on every response.

## Core Patterns

### App Setup

```python
from flask import Flask
from routes.audio import audio_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB upload limit
    app.register_blueprint(audio_bp, url_prefix="/api/audio")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
```

### Blueprint (feature-grouped routes)

```python
# routes/audio.py
from flask import Blueprint, request, jsonify

audio_bp = Blueprint("audio", __name__)

@audio_bp.route("/analyze", methods=["POST"])
def analyze():
    ...
```

### File Upload Endpoint

```python
import os
import tempfile
from flask import request, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a", "ogg"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@audio_bp.route("/analyze", methods=["POST"])
def analyze_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = analyze(tmp_path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.unlink(tmp_path)
```

### JSON Request Parsing

```python
@audio_bp.route("/chords", methods=["POST"])
def get_chords():
    data = request.get_json(silent=True)
    if not data or "key" not in data:
        return jsonify({"error": "Missing 'key' field"}), 400

    key = data["key"]
    chords = get_chord_suggestions(key)
    return jsonify({"key": key, "chords": chords}), 200
```

### Error Handlers (register on app)

```python
@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large (max 50MB)"}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500
```

### Standard Response Shape

Always return consistent JSON so the Android client can rely on the shape:

```python
# Success
return jsonify({
    "key": "G Major",
    "bpm": 120,
    "chords": ["G", "C", "D", "Em"]
}), 200

# Error
return jsonify({"error": "human-readable message"}), <4xx or 5xx>
```

## Project Structure

```
backend/
├── app.py              # create_app(), entry point
├── routes/
│   └── audio.py        # audio_bp blueprint
├── services/
│   └── audio_service.py  # librosa analysis logic
├── models/
│   └── analysis.py     # dataclasses (AnalysisResult etc.)
└── requirements.txt
```

## Quick Reference

| Task | How |
|---|---|
| Get uploaded file | `request.files["file"]` |
| Get JSON body | `request.get_json(silent=True)` |
| Get query param | `request.args.get("key", default)` |
| Return JSON | `jsonify({...}), status_code` |
| Group routes | `Blueprint("name", __name__)` |
| Limit upload size | `app.config["MAX_CONTENT_LENGTH"]` |
| Secure filename | `secure_filename(file.filename)` |

## Common Mistakes

- Returning `jsonify(...)` without a status code — always include the second tuple element
- Using `request.json` instead of `request.get_json(silent=True)` — the latter won't raise on bad JSON
- Not validating `Content-Type` for file uploads — check `request.files` before accessing
- Calling `file.save()` without `secure_filename` — path traversal risk
- Keeping temp files on error — always clean up in `finally`
- Running with `debug=True` in production — use an env flag: `app.run(debug=os.getenv("FLASK_DEBUG", "false") == "true")`
