CHORD_MAP: dict[str, list[str]] = {
    "C Major":  ["C", "F", "G", "Am"],
    "G Major":  ["G", "C", "D", "Em"],
    "D Major":  ["D", "G", "A", "Bm"],
    "A Major":  ["A", "D", "E", "F#m"],
    "E Major":  ["E", "A", "B", "C#m"],
    "F Major":  ["F", "Bb", "C", "Dm"],
    "Bb Major": ["Bb", "Eb", "F", "Gm"],
    "A Minor":  ["Am", "Dm", "Em", "C"],
    "E Minor":  ["Em", "Am", "Bm", "G"],
    "D Minor":  ["Dm", "Gm", "Am", "F"],
    "B Minor":  ["Bm", "Em", "F#m", "A"],
}

def get_chord_suggestions(key: str) -> list[str]:
    return CHORD_MAP.get(key, [])
