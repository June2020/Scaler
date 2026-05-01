import librosa
import numpy as np
from models.analysis import AnalysisResult
from utils.chord_map import get_chord_suggestions

PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F",
                 "F#", "G", "G#", "A", "A#", "B"]

def _bpm_from_audio(y: np.ndarray, sr: int) -> int:
    # Isolate percussive component — vocal syllables live in the harmonic layer
    # and cause beat_track to double/quadruple the true tempo on sung input
    _, y_percussive = librosa.effects.hpss(y)

    # Median aggregation is more robust to spurious onset spikes than mean
    onset_env = librosa.onset.onset_strength(
        y=y_percussive, sr=sr, aggregate=np.median
    )
    tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr, start_bpm=100)[0]
    bpm = int(round(float(np.asarray(tempo).item())))

    # Halve if above typical song range — common octave error on vocal input
    if bpm > 180:
        bpm = bpm // 2

    return bpm

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
