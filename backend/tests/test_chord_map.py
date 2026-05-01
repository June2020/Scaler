from utils.chord_map import get_chord_suggestions


def test_c_major_has_all_categories():
    chords = get_chord_suggestions("C Major")
    assert chords["major"] == ["C", "F", "G"]
    assert chords["minor"] == ["Dm", "Em", "Am"]
    assert chords["diminished"] == ["Bdim"]
    assert "Cmaj7" in chords["seventh"]
    assert "G7" in chords["seventh"]
    assert "Bm7b5" in chords["seventh"]
    assert "Csus2" in chords["sus"]
    assert "Gsus4" in chords["sus"]


def test_g_major_has_all_categories():
    chords = get_chord_suggestions("G Major")
    assert chords["major"] == ["G", "C", "D"]
    assert chords["minor"] == ["Am", "Bm", "Em"]
    assert chords["diminished"] == ["F#dim"]
    assert "D7" in chords["seventh"]
    assert "Dsus4" in chords["sus"]


def test_a_minor_has_all_categories():
    chords = get_chord_suggestions("A Minor")
    assert chords["minor"] == ["Am", "Dm", "Em"]
    assert chords["major"] == ["C", "F", "G"]
    assert chords["diminished"] == ["Bdim"]
    assert "Am7" in chords["seventh"]


def test_unknown_key_returns_empty_categories():
    chords = get_chord_suggestions("X#")
    assert chords["major"] == []
    assert chords["minor"] == []
    assert chords["diminished"] == []
    assert chords["seventh"] == []
    assert chords["sus"] == []


def test_seventh_chords_count():
    for key in ["C Major", "G Major", "D Major", "A Minor"]:
        chords = get_chord_suggestions(key)
        assert len(chords["seventh"]) == 7, f"{key} should have 7 seventh chords"


def test_sus_chords_count():
    for key in ["C Major", "F Major", "Bb Major"]:
        chords = get_chord_suggestions(key)
        assert len(chords["sus"]) == 6, f"{key} should have 6 sus chords (sus2+sus4 on I, IV, V)"
