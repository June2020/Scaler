import librosa
import numpy as np
from models.analysis import AnalysisResult
from utils.chord_map import get_chord_suggestions

PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F",
                 "F#", "G", "G#", "A", "A#", "B"]

def _bpm_from_audio(y: np.ndarray, sr: int) -> int:
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    # tempo may be a 0-d or 1-d numpy array depending on librosa version;
    # extract the scalar with .item() before converting to avoid DeprecationWarning
    return int(round(float(np.asarray(tempo).item())))

def _key_from_audio(y: np.ndarray, sr: int) -> str:
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    key_index = int(np.argmax(chroma_mean))
    note = PITCH_CLASSES[key_index]
    return f"{note} Major"

def detect_bpm(file_path: str) -> int:
    y, sr = librosa.load(file_path, sr=None)
    return _bpm_from_audio(y, sr)

def detect_key(file_path: str) -> str:
    y, sr = librosa.load(file_path, sr=None)
    return _key_from_audio(y, sr)

def analyze_audio(file_path: str) -> AnalysisResult:
    y, sr = librosa.load(file_path, sr=None)
    key = _key_from_audio(y, sr)
    bpm = _bpm_from_audio(y, sr)
    chords = get_chord_suggestions(key)
    return AnalysisResult(key=key, bpm=bpm, chords=chords)
