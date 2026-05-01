# backend/tests/test_routes.py
import io
import numpy as np
import soundfile as sf

def make_wav_bytes() -> bytes:
    sr = 22050
    t = np.linspace(0, 3, sr * 3, endpoint=False)
    audio = 0.5 * np.sin(2 * np.pi * 440 * t)
    buf = io.BytesIO()
    sf.write(buf, audio, sr, format="WAV")
    buf.seek(0)
    return buf.read()

def test_analyze_returns_200(client):
    data = {"file": (io.BytesIO(make_wav_bytes()), "test.wav")}
    response = client.post(
        "/api/audio/analyze",
        content_type="multipart/form-data",
        data=data
    )
    assert response.status_code == 200

def test_analyze_response_has_required_fields(client):
    data = {"file": (io.BytesIO(make_wav_bytes()), "test.wav")}
    response = client.post(
        "/api/audio/analyze",
        content_type="multipart/form-data",
        data=data
    )
    json_data = response.get_json()
    assert "key" in json_data
    assert "bpm" in json_data
    assert "chords" in json_data
    chords = json_data["chords"]
    assert "major" in chords
    assert "minor" in chords
    assert "diminished" in chords
    assert "seventh" in chords
    assert "sus" in chords

def test_analyze_missing_file_returns_400(client):
    response = client.post("/api/audio/analyze", content_type="multipart/form-data", data={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_analyze_invalid_extension_returns_400(client):
    data = {"file": (io.BytesIO(b"fake"), "test.txt")}
    response = client.post(
        "/api/audio/analyze",
        content_type="multipart/form-data",
        data=data
    )
    assert response.status_code == 400
