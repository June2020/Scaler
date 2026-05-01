from models.analysis import AnalysisResult

SAMPLE_CHORDS = {
    "major":      ["C", "F", "G"],
    "minor":      ["Dm", "Em", "Am"],
    "diminished": ["Bdim"],
    "seventh":    ["Cmaj7", "Dm7", "Em7", "Fmaj7", "G7", "Am7", "Bm7b5"],
    "sus":        ["Csus2", "Csus4", "Fsus2", "Fsus4", "Gsus2", "Gsus4"],
}


def test_analysis_result_fields():
    result = AnalysisResult(key="C Major", bpm=90, chords=SAMPLE_CHORDS)
    assert result.key == "C Major"
    assert result.bpm == 90
    assert result.chords == SAMPLE_CHORDS


def test_analysis_result_to_dict():
    result = AnalysisResult(key="C Major", bpm=90, chords=SAMPLE_CHORDS)
    d = result.to_dict()
    assert d["key"] == "C Major"
    assert d["bpm"] == 90
    assert d["chords"]["major"] == ["C", "F", "G"]
    assert d["chords"]["minor"] == ["Dm", "Em", "Am"]
    assert d["chords"]["diminished"] == ["Bdim"]
    assert len(d["chords"]["seventh"]) == 7
    assert len(d["chords"]["sus"]) == 6
