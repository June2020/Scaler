"""
Diatonic chord map for all 12 major keys.
Each key maps to a dict with chord categories:
  major      — I, IV, V  (major triads)
  minor      — IIm, IIIm, VIm  (minor triads)
  diminished — VIIdim
  seventh    — Imaj7, IIm7, IIIm7, IVmaj7, V7, VIm7, VIIm7b5
  sus        — sus2 and sus4 on I, IV, V
"""

ChordMap = dict[str, dict[str, list[str]]]

CHORD_MAP: ChordMap = {
    "C Major": {
        "major":      ["C", "F", "G"],
        "minor":      ["Dm", "Em", "Am"],
        "diminished": ["Bdim"],
        "seventh":    ["Cmaj7", "Dm7", "Em7", "Fmaj7", "G7", "Am7", "Bm7b5"],
        "sus":        ["Csus2", "Csus4", "Fsus2", "Fsus4", "Gsus2", "Gsus4"],
    },
    "G Major": {
        "major":      ["G", "C", "D"],
        "minor":      ["Am", "Bm", "Em"],
        "diminished": ["F#dim"],
        "seventh":    ["Gmaj7", "Am7", "Bm7", "Cmaj7", "D7", "Em7", "F#m7b5"],
        "sus":        ["Gsus2", "Gsus4", "Csus2", "Csus4", "Dsus2", "Dsus4"],
    },
    "D Major": {
        "major":      ["D", "G", "A"],
        "minor":      ["Em", "F#m", "Bm"],
        "diminished": ["C#dim"],
        "seventh":    ["Dmaj7", "Em7", "F#m7", "Gmaj7", "A7", "Bm7", "C#m7b5"],
        "sus":        ["Dsus2", "Dsus4", "Gsus2", "Gsus4", "Asus2", "Asus4"],
    },
    "A Major": {
        "major":      ["A", "D", "E"],
        "minor":      ["Bm", "C#m", "F#m"],
        "diminished": ["G#dim"],
        "seventh":    ["Amaj7", "Bm7", "C#m7", "Dmaj7", "E7", "F#m7", "G#m7b5"],
        "sus":        ["Asus2", "Asus4", "Dsus2", "Dsus4", "Esus2", "Esus4"],
    },
    "E Major": {
        "major":      ["E", "A", "B"],
        "minor":      ["F#m", "G#m", "C#m"],
        "diminished": ["D#dim"],
        "seventh":    ["Emaj7", "F#m7", "G#m7", "Amaj7", "B7", "C#m7", "D#m7b5"],
        "sus":        ["Esus2", "Esus4", "Asus2", "Asus4", "Bsus2", "Bsus4"],
    },
    "B Major": {
        "major":      ["B", "E", "F#"],
        "minor":      ["C#m", "D#m", "G#m"],
        "diminished": ["A#dim"],
        "seventh":    ["Bmaj7", "C#m7", "D#m7", "Emaj7", "F#7", "G#m7", "A#m7b5"],
        "sus":        ["Bsus2", "Bsus4", "Esus2", "Esus4", "F#sus2", "F#sus4"],
    },
    "F# Major": {
        "major":      ["F#", "B", "C#"],
        "minor":      ["G#m", "A#m", "D#m"],
        "diminished": ["E#dim"],
        "seventh":    ["F#maj7", "G#m7", "A#m7", "Bmaj7", "C#7", "D#m7", "E#m7b5"],
        "sus":        ["F#sus2", "F#sus4", "Bsus2", "Bsus4", "C#sus2", "C#sus4"],
    },
    "F Major": {
        "major":      ["F", "Bb", "C"],
        "minor":      ["Gm", "Am", "Dm"],
        "diminished": ["Edim"],
        "seventh":    ["Fmaj7", "Gm7", "Am7", "Bbmaj7", "C7", "Dm7", "Em7b5"],
        "sus":        ["Fsus2", "Fsus4", "Bbsus2", "Bbsus4", "Csus2", "Csus4"],
    },
    "Bb Major": {
        "major":      ["Bb", "Eb", "F"],
        "minor":      ["Cm", "Dm", "Gm"],
        "diminished": ["Adim"],
        "seventh":    ["Bbmaj7", "Cm7", "Dm7", "Ebmaj7", "F7", "Gm7", "Am7b5"],
        "sus":        ["Bbsus2", "Bbsus4", "Ebsus2", "Ebsus4", "Fsus2", "Fsus4"],
    },
    "Eb Major": {
        "major":      ["Eb", "Ab", "Bb"],
        "minor":      ["Fm", "Gm", "Cm"],
        "diminished": ["Ddim"],
        "seventh":    ["Ebmaj7", "Fm7", "Gm7", "Abmaj7", "Bb7", "Cm7", "Dm7b5"],
        "sus":        ["Ebsus2", "Ebsus4", "Absus2", "Absus4", "Bbsus2", "Bbsus4"],
    },
    "Ab Major": {
        "major":      ["Ab", "Db", "Eb"],
        "minor":      ["Bbm", "Cm", "Fm"],
        "diminished": ["Gdim"],
        "seventh":    ["Abmaj7", "Bbm7", "Cm7", "Dbmaj7", "Eb7", "Fm7", "Gm7b5"],
        "sus":        ["Absus2", "Absus4", "Dbsus2", "Dbsus4", "Ebsus2", "Ebsus4"],
    },
    "Db Major": {
        "major":      ["Db", "Gb", "Ab"],
        "minor":      ["Ebm", "Fm", "Bbm"],
        "diminished": ["Cdim"],
        "seventh":    ["Dbmaj7", "Ebm7", "Fm7", "Gbmaj7", "Ab7", "Bbm7", "Cm7b5"],
        "sus":        ["Dbsus2", "Dbsus4", "Gbsus2", "Gbsus4", "Absus2", "Absus4"],
    },
    # Enharmonic aliases
    "C# Major": {
        "major":      ["C#", "F#", "G#"],
        "minor":      ["D#m", "E#m", "A#m"],
        "diminished": ["B#dim"],
        "seventh":    ["C#maj7", "D#m7", "E#m7", "F#maj7", "G#7", "A#m7", "B#m7b5"],
        "sus":        ["C#sus2", "C#sus4", "F#sus2", "F#sus4", "G#sus2", "G#sus4"],
    },
    "D# Major": {
        "major":      ["D#", "G#", "A#"],
        "minor":      ["Fm", "Gm", "Cm"],
        "diminished": ["D#dim"],
        "seventh":    ["D#maj7", "Fm7", "Gm7", "G#maj7", "A#7", "Cm7", "Dm7b5"],
        "sus":        ["D#sus2", "D#sus4", "G#sus2", "G#sus4", "A#sus2", "A#sus4"],
    },
    "G# Major": {
        "major":      ["G#", "C#", "D#"],
        "minor":      ["A#m", "Cm", "Fm"],
        "diminished": ["Gdim"],
        "seventh":    ["G#maj7", "A#m7", "Cm7", "C#maj7", "D#7", "Fm7", "Gm7b5"],
        "sus":        ["G#sus2", "G#sus4", "C#sus2", "C#sus4", "D#sus2", "D#sus4"],
    },
    "A# Major": {
        "major":      ["A#", "D#", "F"],
        "minor":      ["Cm", "Dm", "Gm"],
        "diminished": ["Adim"],
        "seventh":    ["A#maj7", "Cm7", "Dm7", "D#maj7", "F7", "Gm7", "Am7b5"],
        "sus":        ["A#sus2", "A#sus4", "D#sus2", "D#sus4", "Fsus2", "Fsus4"],
    },
    # Natural minor keys
    "A Minor": {
        "major":      ["C", "F", "G"],
        "minor":      ["Am", "Dm", "Em"],
        "diminished": ["Bdim"],
        "seventh":    ["Am7", "Bm7b5", "Cmaj7", "Dm7", "Em7", "Fmaj7", "G7"],
        "sus":        ["Asus2", "Asus4", "Dsus2", "Dsus4", "Esus2", "Esus4"],
    },
    "E Minor": {
        "major":      ["G", "C", "D"],
        "minor":      ["Em", "Am", "Bm"],
        "diminished": ["F#dim"],
        "seventh":    ["Em7", "F#m7b5", "Gmaj7", "Am7", "Bm7", "Cmaj7", "D7"],
        "sus":        ["Esus2", "Esus4", "Asus2", "Asus4", "Bsus2", "Bsus4"],
    },
    "D Minor": {
        "major":      ["F", "Bb", "C"],
        "minor":      ["Dm", "Gm", "Am"],
        "diminished": ["Edim"],
        "seventh":    ["Dm7", "Em7b5", "Fmaj7", "Gm7", "Am7", "Bbmaj7", "C7"],
        "sus":        ["Dsus2", "Dsus4", "Gsus2", "Gsus4", "Asus2", "Asus4"],
    },
    "B Minor": {
        "major":      ["D", "G", "A"],
        "minor":      ["Bm", "Em", "F#m"],
        "diminished": ["A#dim"],
        "seventh":    ["Bm7", "C#m7b5", "Dmaj7", "Em7", "F#m7", "Gmaj7", "A7"],
        "sus":        ["Bsus2", "Bsus4", "Esus2", "Esus4", "F#sus2", "F#sus4"],
    },
}


def get_chord_suggestions(key: str) -> dict[str, list[str]]:
    """Return categorized chord suggestions for a key, or empty categories if unknown."""
    empty: dict[str, list[str]] = {
        "major": [], "minor": [], "diminished": [], "seventh": [], "sus": []
    }
    return CHORD_MAP.get(key, empty)
