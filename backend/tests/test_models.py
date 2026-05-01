from models.analysis import AnalysisResult

def test_analysis_result_fields():
    result = AnalysisResult(key="G Major", bpm=120, chords=["G", "C", "D", "Em"])
    assert result.key == "G Major"
    assert result.bpm == 120
    assert result.chords == ["G", "C", "D", "Em"]

def test_analysis_result_to_dict():
    result = AnalysisResult(key="C Major", bpm=90, chords=["C", "F", "G", "Am"])
    d = result.to_dict()
    assert d == {"key": "C Major", "bpm": 90, "chords": ["C", "F", "G", "Am"]}
