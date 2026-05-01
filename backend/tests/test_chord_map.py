from utils.chord_map import get_chord_suggestions

def test_g_major_chords():
    assert get_chord_suggestions("G Major") == ["G", "C", "D", "Em"]

def test_c_major_chords():
    assert get_chord_suggestions("C Major") == ["C", "F", "G", "Am"]

def test_unknown_key_returns_empty():
    assert get_chord_suggestions("X#") == []

def test_minor_key():
    assert get_chord_suggestions("A Minor") == ["Am", "Dm", "Em", "C"]
