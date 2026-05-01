CHORD_MAP: dict[str, list[str]] = {
    "C Major":  ["C", "F", "G", "Am"],
    "C# Major": ["C#", "F#", "G#", "A#m"],
    "D Major":  ["D", "G", "A", "Bm"],
    "D# Major": ["D#", "G#", "A#", "Cm"],
    "E Major":  ["E", "A", "B", "C#m"],
    "F Major":  ["F", "Bb", "C", "Dm"],
    "F# Major": ["F#", "B", "C#", "D#m"],
    "G Major":  ["G", "C", "D", "Em"],
    "G# Major": ["G#", "C#", "D#", "Fm"],
    "A Major":  ["A", "D", "E", "F#m"],
    "A# Major": ["A#", "D#", "F", "Gm"],
    "B Major":  ["B", "E", "F#", "G#m"],
    "Bb Major": ["Bb", "Eb", "F", "Gm"],
    "A Minor":  ["Am", "Dm", "Em", "C"],
    "E Minor":  ["Em", "Am", "Bm", "G"],
    "D Minor":  ["Dm", "Gm", "Am", "F"],
    "B Minor":  ["Bm", "Em", "F#m", "A"],
}

def get_chord_suggestions(key: str) -> list[str]:
    return CHORD_MAP.get(key, [])
