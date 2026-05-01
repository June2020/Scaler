import os
import tempfile
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.audio_service import analyze_audio

audio_bp = Blueprint("audio", __name__)

ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a", "ogg", "aac"}

def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@audio_bp.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if not file.filename or not _allowed(file.filename):
        return jsonify({"error": "Unsupported file type. Use wav, mp3, m4a, ogg, or aac"}), 400

    suffix = "." + secure_filename(file.filename).rsplit(".", 1)[1]
    tmp_path = None
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        result = analyze_audio(tmp_path)
        return jsonify(result.to_dict()), 200
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
