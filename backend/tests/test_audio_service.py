import numpy as np
import soundfile as sf
import tempfile
import os
import pytest
from services.audio_service import detect_bpm, detect_key, analyze_audio
from models.analysis import AnalysisResult

SAMPLE_RATE = 22050

@pytest.fixture
def sine_wav_path():
    """10-second 440 Hz pulsed sine wave WAV file.

    A pure continuous sine wave has no onset transients, so librosa.beat.beat_track
    returns 0 BPM.  Gating the tone on for the first 20 % of each beat period
    (120 BPM target) creates regular transients the onset detector can find.
    """
    duration = 10
    bpm_target = 120
    beat_period = 60.0 / bpm_target  # 0.5 s per beat
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    beat_phase = (t % beat_period) / beat_period  # 0..1 within each beat
    envelope = (beat_phase < 0.2).astype(float)   # on for first 20 % of beat
    audio = 0.5 * np.sin(2 * np.pi * 440 * t) * envelope
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, SAMPLE_RATE)
        yield f.name
    os.unlink(f.name)

def test_detect_bpm_returns_int(sine_wav_path):
    bpm = detect_bpm(sine_wav_path)
    assert isinstance(bpm, int)
    assert 40 <= bpm <= 240

def test_detect_key_returns_string(sine_wav_path):
    key = detect_key(sine_wav_path)
    assert isinstance(key, str)
    assert len(key) > 0

def test_analyze_audio_returns_result(sine_wav_path):
    result = analyze_audio(sine_wav_path)
    assert isinstance(result, AnalysisResult)
    assert isinstance(result.key, str)
    assert isinstance(result.bpm, int)
    assert isinstance(result.chords, list)
